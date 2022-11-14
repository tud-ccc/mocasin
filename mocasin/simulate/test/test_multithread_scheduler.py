# Copyright (C) 2022 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Francesco Ratto

from mocasin.simulate.process import (
    RuntimeProcess,
    ProcessState,
    InterruptSource,
)
from mocasin.simulate.scheduler import (
    ContextSwitchMode,
    MultithreadFifoScheduler,
)
from mocasin.simulate.process import RuntimeDataflowProcess

import pytest


context_load_ticks = 4
context_store_ticks = 6
scheduling_delay = 7
workload_ticks = 10

n_thread = 1

base_frequency = 1000000

N_THREADS = [1, 2, 5]


@pytest.fixture(params=N_THREADS)
def mt_processor(request, mocker):
    mt_processor = mocker.Mock()
    mt_processor.name = "Test"
    mt_processor.type = "Test"
    mt_processor.ticks = lambda x: x
    mt_processor.n_threads = request.param
    mt_processor.base_frequency = base_frequency
    return mt_processor


@pytest.fixture
def multithread_scheduler(system, mt_processor):
    mt_processor.context_load_ticks = lambda: context_load_ticks
    mt_processor.context_store_ticks = lambda: context_store_ticks
    return MultithreadFifoScheduler(
        "sched",
        mt_processor,
        ContextSwitchMode.NEVER,
        0,
        system,
        mt_processor.n_threads,
    )


def mock_process_workload(env, process, ticks):
    assert process.check_state(ProcessState.RUNNING)
    start_time = env.now
    while 1:
        interrupt = process._interrupt
        ticks_processed = env.now - start_time
        yield env.any_of([env.timeout(ticks - ticks_processed), interrupt])
        if interrupt.processed:
            if interrupt.value == InterruptSource.PREEMPT:
                process._deactivate()
                break
            elif interrupt.value == InterruptSource.ADAPT:
                process._interrupt = env.event()
            else:
                pass
        else:
            process._finish()
            break


@pytest.fixture
def processes(app, env, mt_processor, mocker):
    processes = [RuntimeProcess(f"test_proc{i}", app) for i in range(0, 5)]
    for i in range(0, len(processes)):
        processes[i].workload = mocker.Mock(
            side_effect=lambda i=i: mock_process_workload(
                env, processes[i], workload_ticks * (i + 1)
            )
        )
        processes[i].processor = mocker.Mock(return_value=mt_processor)
    return processes


class TestMultithreadScheduler:
    def test_init(self, multithread_scheduler):
        assert multithread_scheduler.name == "sched"
        assert len(multithread_scheduler.current_processes) == 0
        assert len(multithread_scheduler._processes) == 0
        assert len(multithread_scheduler._ready_queue) == 0
        assert not multithread_scheduler.process_ready.triggered
        assert not multithread_scheduler.process_ready.processed

    def test_add_process(self, multithread_scheduler, process, state, env):
        env.run(1)  # start simulation to initialize the process
        process._transition(state)
        env.run(2)
        if state == "FINISHED" or state == "RUNNING":
            with pytest.raises(RuntimeError):
                multithread_scheduler.add_process(process)
        else:
            multithread_scheduler.add_process(process)
            env.run(3)
            assert len(multithread_scheduler.current_processes) == 0
            if state == "READY":
                assert len(multithread_scheduler._ready_queue) == 1
            else:
                assert len(multithread_scheduler._ready_queue) == 0
            assert len(multithread_scheduler._processes) == 1
            assert process in multithread_scheduler._processes
            assert process.processor is None
            assert process._state == getattr(ProcessState, state)

    def test_process_becomes_ready(self, multithread_scheduler, process, env):
        ready_event = multithread_scheduler.process_ready
        env.run(1)  # start simulation to initialize the process
        multithread_scheduler.add_process(process)
        process.start()
        env.run(2)
        assert ready_event.triggered
        assert ready_event.processed
        assert len(multithread_scheduler._ready_queue) == 1
        assert process in multithread_scheduler._ready_queue

    def test_processes_become_ready(
        self, multithread_scheduler, processes, env
    ):
        env.run()  # start simulation to initialize the process
        for p in processes:
            ready_event = multithread_scheduler.process_ready
            multithread_scheduler.add_process(p)
            p.start()
            env.run()
            assert ready_event.triggered
            assert ready_event.processed
            assert p is multithread_scheduler._ready_queue[-1]
        assert len(multithread_scheduler._ready_queue) == len(processes)
        assert len(multithread_scheduler._processes) == len(processes)

    def call_run(self, multithread_scheduler, processes, env, mocker):
        # initialize the ready queue
        self.test_processes_become_ready(multithread_scheduler, processes, env)
        env.process(multithread_scheduler.run())
        env.run()

    def test_run(self, multithread_scheduler, processes, env, mocker):
        # this test does not consider performance adaptation
        self.call_run(multithread_scheduler, processes, env, mocker)
        if (
            multithread_scheduler._processor.n_threads == 1
        ):  # same of a single thread scheduler
            assert env.now == sum(range(1, len(processes) + 1)) * workload_ticks
        elif (
            multithread_scheduler._processor.n_threads == 5
        ):  # all processes in parallel
            assert env.now == len(processes) * workload_ticks
        elif (
            multithread_scheduler._processor.n_threads == 2
        ):  # 90 is obtained with (simple) manual scheduling
            assert env.now == 90

    def test_remove_process(self, multithread_scheduler, env, app, mocker):
        proc_a = RuntimeDataflowProcess("test_proc_a", app)
        proc_b = RuntimeDataflowProcess("test_proc_b", app)
        env.run(1)  # start simulation to initialize the processes

        # add the processes
        multithread_scheduler.add_process(proc_a)
        multithread_scheduler.add_process(proc_b)

        assert len(multithread_scheduler._ready_queue) == 0
        assert len(multithread_scheduler._processes) == 2

        # mark proc_b as ready
        proc_b.start()
        env.run(2)

        assert len(multithread_scheduler._ready_queue) == 1
        assert len(multithread_scheduler._processes) == 2

        # remove proc_a
        multithread_scheduler.remove_process(proc_a)
        assert len(multithread_scheduler._ready_queue) == 1
        assert len(multithread_scheduler._processes) == 1

        # try to remove proc_a again
        with pytest.raises(ValueError):
            res = multithread_scheduler.remove_process(proc_a)
            assert res is None
        assert len(multithread_scheduler._ready_queue) == 1
        assert len(multithread_scheduler._processes) == 1

        # remove proc_b
        res = multithread_scheduler.remove_process(proc_b)
        assert res is None
        assert len(multithread_scheduler._ready_queue) == 0
        assert len(multithread_scheduler._processes) == 0

    def test_remove_running_process(
        self, multithread_scheduler, mt_processor, env, app, mocker
    ):
        proc_a = RuntimeDataflowProcess("test_proc_a", app)
        proc_b = RuntimeDataflowProcess("test_proc_b", app)

        # give proc_b a workload
        proc_b.workload = mocker.Mock(
            side_effect=lambda: mock_process_workload(env, proc_b, 10)
        )
        proc_b.processor = mocker.Mock(return_value=mt_processor)

        env.run(1)  # start simulation to initialize the processes

        # add the processes
        multithread_scheduler.add_process(proc_a)
        multithread_scheduler.add_process(proc_b)

        assert len(multithread_scheduler._ready_queue) == 0
        assert len(multithread_scheduler._processes) == 2

        # start the scheduler
        env.process(multithread_scheduler.run())
        env.run(2)

        # mark proc_b as ready
        proc_b.start()
        env.run(5)

        assert proc_b.check_state(ProcessState.RUNNING)

        event = multithread_scheduler.remove_process(proc_b)
        assert proc_b not in multithread_scheduler._processes
        assert proc_b not in multithread_scheduler._ready_queue
        assert event is not None
        assert not event.triggered

        env.run(6)
        assert proc_b.check_state(ProcessState.READY)
        assert proc_b not in multithread_scheduler._processes
        assert proc_b not in multithread_scheduler._ready_queue
        assert event.triggered

    def test_scheduling_delay(
        self, multithread_scheduler, processes, env, mocker
    ):
        multithread_scheduler._scheduling_cycles = scheduling_delay
        self.call_run(multithread_scheduler, processes, env, mocker)
        if (
            multithread_scheduler._processor.n_threads == 1
        ):  # same of a single thread scheduler
            assert env.now == (
                sum(range(1, len(processes) + 1)) * workload_ticks
                + len(processes) * scheduling_delay
            )
        elif (
            multithread_scheduler._processor.n_threads == 5
        ):  # all processes in parallel
            assert (
                env.now == (len(processes) * workload_ticks) + scheduling_delay
            )
        elif (
            multithread_scheduler._processor.n_threads == 2
        ):  # 90 is obtained with (simple) manual scheduling
            assert env.now == 90 + (3 * scheduling_delay)

    def test_average_load_idle(self, multithread_scheduler, env, mocker):
        env.process(multithread_scheduler.run())
        env.run(1000000000000)  # simulate 1 second
        assert len(multithread_scheduler.current_processes) == 0
        assert multithread_scheduler.average_load(1) == 0.0
        assert multithread_scheduler.average_load(1000) == 0.0
        assert multithread_scheduler.average_load(1000000000000) == 0.0

    def test_average_load_active(
        self, multithread_scheduler, env, mocker, mt_processor, processes
    ):
        process = processes[0]
        process.workload = mocker.Mock(
            side_effect=lambda: mock_process_workload(
                env, process, 2000000000000
            )
        )
        process.processor = mocker.Mock(return_value=mt_processor)

        # start the process
        self.test_processes_become_ready(multithread_scheduler, [process], env)

        # start the scheduler
        env.process(multithread_scheduler.run())

        env.run(1000000000000)  # simulate 1 second

        assert multithread_scheduler.average_load(1) == 1.0
        assert multithread_scheduler.average_load(1000) == 1.0
        assert multithread_scheduler.average_load(1000000000000) == 1.0
        assert multithread_scheduler.average_load(10000000000000) == 0.1

    def test_frequency_change(
        self, multithread_scheduler, env, mocker, mt_processor, processes
    ):
        self.test_processes_become_ready(multithread_scheduler, processes, env)
        env.process(multithread_scheduler.run())
        env.run(1)
        if multithread_scheduler._processor.n_threads == 1:
            assert multithread_scheduler.n_running_threads == 1
            assert mt_processor.frequency == base_frequency
        elif multithread_scheduler._processor.n_threads == 2:
            assert multithread_scheduler.n_running_threads == 2
            assert mt_processor.frequency == base_frequency / 2
        elif multithread_scheduler._processor.n_threads == 5:
            assert multithread_scheduler.n_running_threads == 5
            assert mt_processor.frequency == base_frequency / 5

        env.run(20)
        if multithread_scheduler._processor.n_threads == 5:
            # the first process has finished
            assert multithread_scheduler.n_running_threads == 4
            assert mt_processor.frequency == base_frequency / 4

        env.run()
        assert multithread_scheduler.n_running_threads == 0
        assert mt_processor.frequency == base_frequency
