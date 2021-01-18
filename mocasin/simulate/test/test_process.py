# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import pytest
from mocasin.common.trace import TraceGenerator, TraceSegment
from mocasin.simulate.process import ProcessState, RuntimeProcess


class TestRuntimeProcess(object):
    def test_init_process_state(self, process):
        assert process.name == "test_proc"
        assert process.processor is None
        assert process._state == ProcessState.CREATED

    def test_transitions(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process

        callback = mocker.Mock()
        event = getattr(process, state.lower())
        event.callbacks.append(callback)

        process._transition(state)
        assert process._state == getattr(ProcessState, state)

        process.env.run(2)  # continue simulation so that callback is called
        callback.assert_called_once_with(event)
        assert event.ok and event.processed

    def test_transition_invalid(self, process):
        with pytest.raises(RuntimeError):
            process._transition("INVALID")

    def test_start(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        if state == "CREATED":
            process.processor = mocker.Mock()
            process.start()
            process.env.run(3)
            assert process._state == ProcessState.READY
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process.start()

    def test_activate(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        processor = mocker.Mock()
        if state == "READY":
            process.activate(processor)
            process.env.run(3)
            assert process._state == ProcessState.RUNNING
            assert process.processor is processor
        else:
            with pytest.raises(AssertionError):
                process.activate(processor)

    def test_deactivate(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        if state == "RUNNING":
            process.processor = mocker.Mock()
            process._deactivate()
            process.env.run(3)
            assert process._state == ProcessState.READY
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process._block()

    def test_finish(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        if state == "RUNNING":
            process.processor = mocker.Mock()
            process._finish()
            process.env.run(3)
            assert process._state == ProcessState.FINISHED
            assert process.processor is None
        else:
            process._finish()
            process.env.run(3)
            assert process._state == ProcessState.FINISHED

    def test_block(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        if state == "RUNNING":
            process.processor = mocker.Mock()
            process._block()
            process.env.run(3)
            assert process._state == ProcessState.BLOCKED
            assert process.processor is None
        else:
            with pytest.raises(AssertionError):
                process._block()

    def test_unblock(self, process, state, mocker):
        process.env.run(1)  # start simulation to initialze the process
        process._transition(state)
        process.env.run(2)
        if state == "BLOCKED":
            process.processor = mocker.Mock()
            process.unblock()
            process.env.run(3)
            assert process._state == ProcessState.READY
            assert process.processor is None
        elif state == "FINISHED":
            process.unblock()
            process.env.run(3)
            assert process._state == ProcessState.FINISHED
        else:
            with pytest.raises(AssertionError):
                process.unblock()


@pytest.fixture
def full_channel(env, mocker):
    channel = mocker.Mock()
    channel.can_consume = lambda x, y: True
    channel.can_produce = lambda x, y: False
    channel.consume = lambda x, y: (yield env.timeout(100))
    channel.produce = lambda x, y: (yield env.timeout(1000))
    return channel


@pytest.fixture
def empty_channel(env, mocker):
    channel = mocker.Mock()
    channel.can_consume = lambda x, y: False
    channel.can_produce = lambda x, y: True
    channel.consume = lambda x, y: (yield env.timeout(100))
    channel.produce = lambda x, y: (yield env.timeout(1000))
    return channel


class TestRuntimeDataflowProcess:
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
            t.read_from_channel = "chan"
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
            t.write_to_channel = "chan"
            t.n_tokens = 1
            if self.i == 5:
                t.terminate = True
            self.i += 1
            return t

    class InvalidTraceGenerator(TraceGenerator):
        def next_segment(self, process_name, processor_type):
            t = TraceSegment()
            t.processing_cycles = 10
            t.write_to_channel = "chan1"
            t.n_tokens = 1
            t.read_from_channel = "chan2"
            t.terminate = True
            return t

    def _run(
        self,
        env,
        dataflow_process,
        processor,
        trace_generator=None,
        channel=None,
    ):
        dataflow_process._trace_generator = trace_generator
        env.run()
        dataflow_process._channels["chan"] = channel
        dataflow_process.start()
        env.run()
        dataflow_process.activate(processor)
        env.run()
        finished = env.process(dataflow_process.workload())
        env.run(finished)

    def test_workload_terminate(self, env, dataflow_process, processor):
        self._run(
            env, dataflow_process, processor, self.TerminateTraceGenerator()
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 0

    def test_workload_processing(self, env, dataflow_process, processor):
        self._run(
            env, dataflow_process, processor, self.ProcessingTraceGenerator()
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 15

    def test_workload_read(
        self, env, dataflow_process, processor, full_channel
    ):
        self._run(
            env,
            dataflow_process,
            processor,
            self.ReadTraceGenerator(),
            full_channel,
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 515

    def test_workload_write(
        self, env, dataflow_process, processor, empty_channel
    ):
        self._run(
            env,
            dataflow_process,
            processor,
            self.WriteTraceGenerator(),
            empty_channel,
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 5015

    def test_workload_read_block(
        self, env, dataflow_process, processor, empty_channel
    ):
        dataflow_process._trace_generator = self.ReadTraceGenerator()
        env.run()
        dataflow_process._channels["chan"] = empty_channel
        dataflow_process.start()
        env.run()
        dataflow_process.activate(processor)
        env.run()
        finished = env.process(dataflow_process.workload())
        env.run(finished)
        assert dataflow_process._state == ProcessState.BLOCKED
        assert env.now == 1

    def test_workload_write_block(
        self, env, dataflow_process, processor, full_channel
    ):
        self._run(
            env,
            dataflow_process,
            processor,
            self.WriteTraceGenerator(),
            full_channel,
        )
        assert dataflow_process._state == ProcessState.BLOCKED
        assert env.now == 1

    def _run_after_block(self, env, dataflow_process, processor):
        dataflow_process.unblock()
        env.run()
        dataflow_process.activate(processor)
        env.run()
        finished = env.process(dataflow_process.workload())
        env.run(finished)

    def test_workload_read_resume(
        self, env, dataflow_process, processor, empty_channel, full_channel
    ):
        self.test_workload_read_block(
            env, dataflow_process, processor, empty_channel
        )
        dataflow_process._channels["chan"] = full_channel
        self._run_after_block(env, dataflow_process, processor)
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 515

    def test_workload_write_resume(
        self, env, dataflow_process, processor, empty_channel, full_channel
    ):
        self.test_workload_write_block(
            env, dataflow_process, processor, full_channel
        )
        dataflow_process._channels["chan"] = empty_channel
        self._run_after_block(env, dataflow_process, processor)
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 5015

    def test_workload_invalid(self, env, dataflow_process, processor):
        with pytest.raises(RuntimeError):
            self._run(
                env, dataflow_process, processor, self.InvalidTraceGenerator()
            )

    def test_connect_to_incomming_channel(self, dataflow_process, mocker):
        channel = mocker.Mock()
        channel.name = "test"
        dataflow_process.connect_to_incomming_channel(channel)
        assert dataflow_process._channels["test"] is channel
        channel.add_sink.assert_called_once_with(dataflow_process)

    def test_connect_to_outgoing_channel(self, dataflow_process, mocker):
        channel = mocker.Mock()
        channel.name = "test"
        dataflow_process.connect_to_outgoing_channel(channel)
        assert dataflow_process._channels["test"] is channel
        channel.set_src.assert_called_once_with(dataflow_process)


def test_default_workload(app, mocker):
    process = RuntimeProcess("test", app)
    process.start()
    app.env.run()
    process.activate(mocker.Mock())
    with pytest.raises(NotImplementedError):
        app.env.process(process.workload())
        app.env.run()
