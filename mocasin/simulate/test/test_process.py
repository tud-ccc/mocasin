# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import pytest
import weakref

from mocasin.common.trace import (
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)
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
    def empty_trace_generator(self):
        return
        yield

    def processing_trace_generator(self):
        for i in range(1, 6):
            yield ComputeSegment({"Test": i})

    def read_trace_generator(self):
        for i in range(1, 6):
            yield ComputeSegment(processor_cycles={"Test": i})
            yield ReadTokenSegment(channel="chan", num_tokens=1)

    def write_trace_generator(self):
        for i in range(1, 6):
            yield ComputeSegment(processor_cycles={"Test": i})
            yield WriteTokenSegment(channel="chan", num_tokens=1)

    def preemption_trace_generator(self):
        yield ComputeSegment({"Test": 10, "Test2": 20})

    def _run(
        self,
        env,
        dataflow_process,
        processor,
        trace=None,
        channel=None,
    ):
        dataflow_process._trace = trace
        env.run()
        dataflow_process._channels["chan"] = (
            weakref.ref(channel) if channel else None
        )
        dataflow_process.start()
        env.run()
        dataflow_process.activate(processor)
        env.run()
        finished = env.process(dataflow_process.workload())
        env.run(finished)

    def test_workload_terminate(self, env, dataflow_process, processor):
        self._run(
            env, dataflow_process, processor, self.empty_trace_generator()
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 0

    def test_workload_processing(self, env, dataflow_process, processor):
        self._run(
            env, dataflow_process, processor, self.processing_trace_generator()
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 15

    def test_preemption(self, env, dataflow_process, processor, processor2):
        # monkey patch the process to add a trace
        dataflow_process._trace = self.preemption_trace_generator()
        dataflow_process._total_cycles = {"Test": 10, "Test2": 20}
        dataflow_process._remaining_compute_cycles = {"Test": 0, "Test2": 0}

        env.run()
        dataflow_process.start()
        env.run()
        dataflow_process.activate(processor)
        assert dataflow_process.processor is processor
        env.run()
        env.process(dataflow_process.workload())
        env.run(5)
        dataflow_process.preempt()
        env.run(10)

        assert dataflow_process.processor is None
        assert dataflow_process._remaining_compute_cycles["Test"] == 5
        assert dataflow_process._remaining_compute_cycles["Test2"] == 10
        assert dataflow_process.get_progress() == 0.5

        # continue execution on processor2 for 5 cycles (10 ticks)
        dataflow_process.activate(processor2)
        env.run(15)
        env.process(dataflow_process.workload())
        assert dataflow_process.processor is processor2
        env.run(25)
        dataflow_process.preempt()
        env.run(26)

        assert dataflow_process.processor is None
        assert dataflow_process._remaining_compute_cycles["Test"] == 3
        assert dataflow_process._remaining_compute_cycles["Test2"] == 5
        assert dataflow_process.get_progress() == 0.725

        dataflow_process.activate(processor2)
        env.run(30)
        finished = env.process(dataflow_process.workload())
        env.run(finished)

        assert dataflow_process._remaining_compute_cycles is None
        assert dataflow_process._remaining_compute_cycles is None

        assert dataflow_process.get_progress() == 1.0

    def test_workload_read(
        self, env, dataflow_process, processor, full_channel
    ):
        self._run(
            env,
            dataflow_process,
            processor,
            self.read_trace_generator(),
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
            self.write_trace_generator(),
            empty_channel,
        )
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 5015

    def test_workload_read_block(
        self, env, dataflow_process, processor, empty_channel
    ):
        dataflow_process._trace = self.read_trace_generator()
        env.run()
        dataflow_process._channels["chan"] = weakref.ref(empty_channel)
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
            self.write_trace_generator(),
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
        dataflow_process._channels["chan"] = weakref.ref(full_channel)
        self._run_after_block(env, dataflow_process, processor)
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 515

    def test_workload_write_resume(
        self, env, dataflow_process, processor, empty_channel, full_channel
    ):
        self.test_workload_write_block(
            env, dataflow_process, processor, full_channel
        )
        dataflow_process._channels["chan"] = weakref.ref(empty_channel)
        self._run_after_block(env, dataflow_process, processor)
        assert dataflow_process._state == ProcessState.FINISHED
        assert env.now == 5015

    def test_connect_to_incomming_channel(self, dataflow_process, mocker):
        channel = mocker.Mock()
        channel.name = "test"
        dataflow_process.connect_to_incomming_channel(channel)
        assert dataflow_process._channels["test"]() is channel
        channel.add_sink.assert_called_once_with(dataflow_process)

    def test_connect_to_outgoing_channel(self, dataflow_process, mocker):
        channel = mocker.Mock()
        channel.name = "test"
        dataflow_process.connect_to_outgoing_channel(channel)
        assert dataflow_process._channels["test"]() is channel
        channel.set_src.assert_called_once_with(dataflow_process)


def test_default_workload(app, mocker):
    process = RuntimeProcess("test", app)
    process.start()
    app.env.run()
    process.activate(mocker.Mock())
    with pytest.raises(NotImplementedError):
        app.env.process(process.workload())
        app.env.run()
