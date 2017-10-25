# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from unittest.mock import Mock

import pytest
from pykpn.common.trace import TraceGenerator, TraceSegment
from pykpn.simulate.process import (ProcessState, RuntimeKpnProcess,
    RuntimeProcess)


@pytest.fixture
def kpn_process(env):
    return RuntimeKpnProcess('test', Mock(), env, start_at_tick=1000)


@pytest.fixture
def base_process(env):
    return RuntimeProcess('test', env)


@pytest.fixture(params=['base', 'kpn'])
def process(request, env):
    if request.param == 'base':
        proc = base_process(env)
    elif request.param == 'kpn':
        proc = kpn_process(env)
    else:
        raise ValueError('Unexpected fixture parameter')

    proc.workload = Mock()
    return proc


@pytest.fixture(params=ProcessState.__members__)
def state(request):
    return request.param


class TestRuntimeProcess(object):

    def test_init_process_state(self, process):
        assert process.name == 'test'
        assert process.processor is None
        assert process._state == ProcessState.CREATED

    def test_transitions(self, process, state):
        callback = Mock()
        event = getattr(process, state.lower())
        event.callbacks.append(callback)

        process._transition(state)
        assert process._state == getattr(ProcessState, state)

        process._env.run(1)  # start simulation so that callback is called
        callback.assert_called_once_with(event)

    def test_transition_invalid(self, process):
        with pytest.raises(RuntimeError):
            process._transition('INVALID')

    def test_start(self, process, state):
        process._transition(state)
        process._env.run(1)
        if state == 'CREATED':
            process.processor = Mock()
            process.start()
            process._env.run(2)
            assert process._state == ProcessState.READY
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process.start()

    def test_activate(self, process, state):
        process._transition(state)
        process._env.run(1)
        processor = Mock()
        if state == 'READY':
            process.activate(processor)
            process._env.run(2)
            assert process._state == ProcessState.RUNNING
            assert process.processor is processor
            process.workload.assert_called_once()
        else:
            with pytest.raises(AssertionError):
                process.activate(processor)

    def test_finish(self, process, state):
        process._transition(state)
        process._env.run(1)
        if state == 'RUNNING':
            process.processor = Mock()
            process.finish()
            process._env.run(2)
            assert process._state == ProcessState.FINISHED
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process.finish()

    def test_block(self, process, state):
        process._transition(state)
        process._env.run(1)
        if state == 'RUNNING':
            process.processor = Mock()
            process.block()
            process._env.run(2)
            assert process._state == ProcessState.BLOCKED
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process.block()

    def test_unblock(self, process, state):
        process._transition(state)
        process._env.run(1)
        if state == 'BLOCKED':
            process.processor = Mock()
            process.unblock()
            process._env.run(2)
            assert process._state == ProcessState.READY
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process.unblock()


@pytest.fixture
def processor():
    processor = Mock()
    processor.name = 'Test'
    processor.ticks = lambda x: x
    return processor


@pytest.fixture
def full_channel(env):
    channel = Mock()
    channel.can_consume = lambda x, y: True
    channel.can_produce = lambda x, y: False
    channel.consume = lambda x, y: (yield env.timeout(100))
    channel.produce = lambda x, y: (yield env.timeout(1000))
    return channel


@pytest.fixture
def empty_channel(env):
    channel = Mock()
    channel.can_consume = lambda x, y: False
    channel.can_produce = lambda x, y: True
    channel.consume = lambda x, y: (yield env.timeout(100))
    channel.produce = lambda x, y: (yield env.timeout(1000))
    return channel


class TestRuntimeKpnProcess:

    class TerminateTraceGenerator(TraceGenerator):

        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.terminate = True
            return t

    class ProcessingTraceGenerator(TraceGenerator):

        def __init__(self):
            self.i = 1

        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.processing_cycles = self.i
            if self.i == 5:
                t.terminate = True
            self.i += 1
            return t

    class ReadTraceGenerator(TraceGenerator):

        def __init__(self):
            self.i = 1

        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.processing_cycles = self.i
            t.read_from_channel = 'chan'
            t.n_tokens = 1
            if self.i == 5:
                t.terminate = True
            self.i += 1
            return t

    class WriteTraceGenerator(TraceGenerator):

        def __init__(self):
            self.i = 1

        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.processing_cycles = self.i
            t.write_to_channel = 'chan'
            t.n_tokens = 1
            if self.i == 5:
                t.terminate = True
            self.i += 1
            return t

    class InvalidTraceGenerator(TraceGenerator):

        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.processing_cycles = 10
            t.write_to_channel = 'chan1'
            t.n_tokens = 1
            t.read_from_channel = 'chan2'
            t.terminate = True
            return t

    def _run(self, env, kpn_process, processor, trace_generator=None,
             channel=None):
        kpn_process._trace_generator = trace_generator
        env.run()
        kpn_process._channels['chan'] = channel
        kpn_process.activate(processor)
        env.run()

    def test_auto_start(self, env, kpn_process):
        event = kpn_process.ready
        env.run()
        assert kpn_process.check_state(ProcessState.READY)
        assert event.ok

    def test_workload_execution(self, env, kpn_process, processor):
        kpn_process.workload = Mock()
        self._run(env, kpn_process, processor)
        kpn_process.workload.assert_called_once()

    def test_workload_terminate(self, env, kpn_process, processor):
        self._run(env, kpn_process, processor, self.TerminateTraceGenerator())
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 1000

    def test_workload_processing(self, env, kpn_process, processor):
        self._run(env, kpn_process, processor, self.ProcessingTraceGenerator())
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 1015

    def test_workload_read(self, env, kpn_process, processor, full_channel):
        self._run(env, kpn_process, processor, self.ReadTraceGenerator(),
                  full_channel)
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 1515

    def test_workload_write(self, env, kpn_process, processor, empty_channel):
        self._run(env, kpn_process, processor, self.WriteTraceGenerator(),
                  empty_channel)
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 6015

    def test_workload_read_block(self, env, kpn_process, processor,
                                 empty_channel):
        kpn_process._trace_generator = self.ReadTraceGenerator()
        env.run()
        kpn_process._channels['chan'] = empty_channel
        kpn_process.activate(processor)
        env.run()
        assert kpn_process._state == ProcessState.BLOCKED
        assert env.now == 1001

    def test_workload_write_block(self, env, kpn_process, processor,
                                  full_channel):
        self._run(env, kpn_process, processor, self.WriteTraceGenerator(),
                  full_channel)
        assert kpn_process._state == ProcessState.BLOCKED
        assert env.now == 1001

    def _run_after_block(self, env, kpn_process, processor):
        kpn_process.unblock()
        env.run()
        kpn_process.activate(processor)
        env.run()

    def test_workload_read_resume(self, env, kpn_process, processor,
                                  empty_channel, full_channel):
        self.test_workload_read_block(env, kpn_process, processor,
                                      empty_channel)
        kpn_process._channels['chan'] = full_channel
        self._run_after_block(env, kpn_process, processor)
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 1515

    def test_workload_write_resume(self, env, kpn_process, processor,
                                   empty_channel, full_channel):
        self.test_workload_write_block(env, kpn_process, processor,
                                       full_channel)
        kpn_process._channels['chan'] = empty_channel
        self._run_after_block(env, kpn_process, processor)
        assert kpn_process._state == ProcessState.FINISHED
        assert env.now == 6015

    def test_workload_invalid(self, env, kpn_process, processor):
        with pytest.raises(RuntimeError):
            self._run(env, kpn_process, processor,
                      self.InvalidTraceGenerator())

    def test_connect_to_incomming_channel(self, kpn_process):
        channel = Mock()
        channel.name = 'test'
        kpn_process.connect_to_incomming_channel(channel)
        assert kpn_process._channels['test'] is channel
        channel.add_sink.assert_called_once_with(kpn_process)

    def test_connect_to_outgoing_channel(self, kpn_process):
        channel = Mock()
        channel.name = 'test'
        kpn_process.connect_to_outgoing_channel(channel)
        assert kpn_process._channels['test'] is channel
        channel.set_src.assert_called_once_with(kpn_process)


def test_default_workload(env):
    process = RuntimeProcess('test', env)
    process.start()
    env.run()
    process.activate(Mock())
    with pytest.raises(NotImplementedError):
        env.run()
