# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


from mocasin.simulate.process import RuntimeProcess, ProcessState
from mocasin.simulate.scheduler import ContextSwitchMode, RuntimeScheduler
from mocasin.simulate.process import RuntimeDataflowProcess


import pytest


context_load_ticks = 4
context_store_ticks = 6
scheduling_delay = 7
workload_ticks = 10


@pytest.fixture
def runtime_scheduler(system, processor):
    processor.context_load_ticks = lambda: context_load_ticks
    processor.context_store_ticks = lambda: context_store_ticks
    return RuntimeScheduler(
        "sched", processor, ContextSwitchMode.NEVER, 0, None, system
    )


def mock_process_workload(env, process, ticks):
    assert process.check_state(ProcessState.RUNNING)
    interrupt = process._interrupt
    yield env.any_of([env.timeout(ticks), interrupt])
    if interrupt.processed:
        process._deactivate()
    else:
        process._finish()


@pytest.fixture
def processes(app, env, mocker):
    processes = [RuntimeProcess(f"test_proc{i}", app) for i in range(0, 5)]
    for i in range(0, len(processes)):
        processes[i].workload = mocker.Mock(
            side_effect=lambda i=i: mock_process_workload(
                env, processes[i], workload_ticks * (i + 1)
            )
        )
    return processes


class TestRuntimeScheduler:
    def test_init(self, runtime_scheduler):
        assert runtime_scheduler.name == "sched"
        assert runtime_scheduler.current_process is None
        assert len(runtime_scheduler._processes) == 0
        assert len(runtime_scheduler._ready_queue) == 0
        assert not runtime_scheduler.process_ready.triggered
        assert not runtime_scheduler.process_ready.processed

    def test_add_process(self, runtime_scheduler, process, state, env):
        env.run(1)  # start simulation to initialize the process
        process._transition(state)
        env.run(2)
        if state == "FINISHED":
            with pytest.raises(RuntimeError):
                runtime_scheduler.add_process(process)
        else:
            runtime_scheduler.add_process(process)
            env.run(3)
            assert runtime_scheduler.current_process is None
            assert len(runtime_scheduler._ready_queue) == 0
            assert len(runtime_scheduler._processes) == 1
            assert process in runtime_scheduler._processes
            assert process.processor is None
            assert process._state == getattr(ProcessState, state)

    def test_process_becomes_ready(self, runtime_scheduler, process, env):
        ready_event = runtime_scheduler.process_ready
        env.run(1)  # start simulation to initialize the process
        runtime_scheduler.add_process(process)
        process.start()
        env.run(2)
        assert ready_event.triggered
        assert ready_event.processed
        assert len(runtime_scheduler._ready_queue) == 1
        assert process in runtime_scheduler._ready_queue

    def test_processes_become_ready(self, runtime_scheduler, processes, env):
        env.run()  # start simulation to initialize the process
        for p in processes:
            ready_event = runtime_scheduler.process_ready
            runtime_scheduler.add_process(p)
            p.start()
            env.run()
            assert ready_event.triggered
            assert ready_event.processed
            assert p is runtime_scheduler._ready_queue[-1]
        assert len(runtime_scheduler._ready_queue) == len(processes)
        assert len(runtime_scheduler._processes) == len(processes)

    def test_default_schedule(self, runtime_scheduler):
        with pytest.raises(NotImplementedError):
            runtime_scheduler.schedule()

    def test_run_empty_schedule(self, runtime_scheduler, env, mocker):
        runtime_scheduler.schedule = mocker.Mock(side_effect=lambda: None)
        env.process(runtime_scheduler.run())
        env.run()
        runtime_scheduler.schedule.assert_called_once()
        assert runtime_scheduler.current_process is None
        assert env.now == 0

    def call_run(self, runtime_scheduler, processes, env, mocker):
        # initialize the ready queue
        self.test_processes_become_ready(runtime_scheduler, processes, env)
        runtime_scheduler.schedule = mocker.Mock(
            side_effect=lambda: runtime_scheduler._ready_queue[0]
            if len(runtime_scheduler._ready_queue) > 0
            else None
        )
        env.process(runtime_scheduler.run())
        env.run()
        runtime_scheduler.schedule.assert_called()
        assert runtime_scheduler.schedule.call_count == len(processes) + 1

    def test_run(self, runtime_scheduler, processes, env, mocker):
        self.call_run(runtime_scheduler, processes, env, mocker)
        assert env.now == sum(range(1, len(processes) + 1)) * workload_ticks

    def test_remove_process(self, runtime_scheduler, env, app, mocker):
        proc_a = RuntimeDataflowProcess("test_proc_a", mocker.Mock(), app)
        proc_b = RuntimeDataflowProcess("test_proc_b", mocker.Mock(), app)
        env.run(1)  # start simulation to initialize the processes

        # add the processes
        runtime_scheduler.add_process(proc_a)
        runtime_scheduler.add_process(proc_b)

        assert len(runtime_scheduler._ready_queue) == 0
        assert len(runtime_scheduler._processes) == 2

        # mark proc_b as ready
        proc_b.start()
        env.run(2)

        assert len(runtime_scheduler._ready_queue) == 1
        assert len(runtime_scheduler._processes) == 2

        # remove proc_a
        runtime_scheduler.remove_process(proc_a)
        assert len(runtime_scheduler._ready_queue) == 1
        assert len(runtime_scheduler._processes) == 1

        # try to remove proc_a again
        with pytest.raises(ValueError):
            res = runtime_scheduler.remove_process(proc_a)
            assert res is None
        assert len(runtime_scheduler._ready_queue) == 1
        assert len(runtime_scheduler._processes) == 1

        # remove proc_b
        res = runtime_scheduler.remove_process(proc_b)
        assert res is None
        assert len(runtime_scheduler._ready_queue) == 0
        assert len(runtime_scheduler._processes) == 0

    def test_remove_running_process(self, runtime_scheduler, env, app, mocker):
        proc_a = RuntimeDataflowProcess("test_proc_a", mocker.Mock(), app)
        proc_b = RuntimeDataflowProcess("test_proc_b", mocker.Mock(), app)

        # give proc_b a workload
        proc_b.workload = mocker.Mock(
            side_effect=lambda: mock_process_workload(env, proc_b, 10)
        )

        # also mock up the schedule function
        runtime_scheduler.schedule = mocker.Mock(
            side_effect=lambda: runtime_scheduler._ready_queue[0]
            if len(runtime_scheduler._ready_queue) > 0
            else None
        )

        env.run(1)  # start simulation to initialize the processes

        # add the processes
        runtime_scheduler.add_process(proc_a)
        runtime_scheduler.add_process(proc_b)

        assert len(runtime_scheduler._ready_queue) == 0
        assert len(runtime_scheduler._processes) == 2

        # start the scheduler
        env.process(runtime_scheduler.run())
        env.run(2)

        # mark proc_b as ready
        proc_b.start()
        env.run(5)

        assert proc_b.check_state(ProcessState.RUNNING)

        event = runtime_scheduler.remove_process(proc_b)
        assert proc_b not in runtime_scheduler._processes
        assert proc_b not in runtime_scheduler._ready_queue
        assert event is not None
        assert not event.triggered

        env.run(6)
        assert proc_b.check_state(ProcessState.READY)
        assert proc_b not in runtime_scheduler._processes
        assert proc_b not in runtime_scheduler._ready_queue
        assert event.triggered

    def test_scheduling_delay(self, runtime_scheduler, processes, env, mocker):
        runtime_scheduler._scheduling_cycles = scheduling_delay
        self.call_run(runtime_scheduler, processes, env, mocker)
        assert env.now == (
            sum(range(1, len(processes) + 1)) * workload_ticks
            + len(processes) * scheduling_delay
        )

    def test_average_load_idle(self, runtime_scheduler, env, mocker):
        runtime_scheduler.schedule = mocker.Mock(side_effect=lambda: None)
        env.process(runtime_scheduler.run())
        env.run(1000000000000)  # simulate 1 second
        assert runtime_scheduler.current_process is None
        assert runtime_scheduler.average_load(1) == 0.0
        assert runtime_scheduler.average_load(1000) == 0.0
        assert runtime_scheduler.average_load(1000000000000) == 0.0

    def test_average_load_active(
        self, runtime_scheduler, env, mocker, processes
    ):
        process = processes[0]
        process.workload = mocker.Mock(
            side_effect=lambda: mock_process_workload(
                env, process, 2000000000000
            )
        )
        # start the process
        self.test_processes_become_ready(runtime_scheduler, [process], env)

        # start the scheduler
        runtime_scheduler.schedule = mocker.Mock(side_effect=lambda: process)
        env.process(runtime_scheduler.run())

        env.run(1000000000000)  # simulate 1 second

        assert runtime_scheduler.current_process is process
        assert runtime_scheduler.average_load(1) == 1.0
        assert runtime_scheduler.average_load(1000) == 1.0
        assert runtime_scheduler.average_load(1000000000000) == 1.0
        assert runtime_scheduler.average_load(10000000000000) == 0.1
