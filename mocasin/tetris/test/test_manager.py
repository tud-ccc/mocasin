# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import pytest

from mocasin.tetris.job_request import JobRequestStatus
from mocasin.tetris.manager_new import ResourceManager
from mocasin.tetris.scheduler.medf import MedfScheduler


def test_manager_new_request(platform, graph, mappings):
    scheduler = MedfScheduler(platform)
    manager = ResourceManager(platform, scheduler)

    assert manager.state_time == 0.0
    assert manager.schedule is None
    assert not manager.requests

    # schedule 0 jobs
    schedule = manager.generate_schedule()
    assert not schedule
    schedule = manager.generate_schedule(force=True)
    assert not schedule

    # schedule three jobs one by one
    for i in range(1, 4):
        request = manager.new_request(graph, mappings, timeout=10.0)
        assert request.status == JobRequestStatus.NEW
        schedule = manager.generate_schedule()
        assert schedule
        assert request.status == JobRequestStatus.ACCEPTED
        assert len(manager.requests) == i
        assert len(manager.accepted_requests()) == i
        assert len(manager.schedule.get_job_mappings()) == i
        assert manager.schedule.start_time == 0.0
        assert manager.schedule.end_time <= 10.0

    # Schedule four jobs at the same time
    requests = []
    for i in range(4, 8):
        request = manager.new_request(graph, mappings, timeout=10.0)
        requests.append(request)
        assert request.status == JobRequestStatus.NEW
        assert len(manager.requests) == i
        assert len(manager.accepted_requests()) == 3
        assert len(manager.schedule.get_job_mappings()) == 3

    schedule = manager.generate_schedule()
    assert schedule
    assert all(r.status == JobRequestStatus.ACCEPTED for r in requests[:3])
    assert requests[3].status == JobRequestStatus.REFUSED
    assert len(manager.requests) == 7
    assert len(manager.accepted_requests()) == 6
    assert len(manager.schedule.get_job_mappings()) == 6
    assert manager.schedule.start_time == 0.0
    assert manager.schedule.end_time <= 10.0


def test_manager_advance_to_time(platform, graph, mappings):
    scheduler = MedfScheduler(platform)
    manager = ResourceManager(platform, scheduler)
    assert manager.state_time == 0.0

    # Advance the manager when it is free
    manager.advance_to_time(5.0)
    assert manager.state_time == 5.0

    # Add a request, check that the schedule's start time is 5.0
    request = manager.new_request(graph, mappings, timeout=5.0)
    schedule = manager.generate_schedule()
    assert schedule == manager.schedule
    assert schedule.start_time == 5.0
    job_end_time = schedule.end_time
    assert job_end_time <= 10.0
    # Check the job state at the beginning of execution
    job = manager.accepted_requests()[0][1]
    assert job.request == request
    assert job.is_ready()
    assert not job.mapping
    assert not job.last_mapping
    assert job.cratio == 0.0

    # Advance the manager within a single segment
    manager.advance_to_time(6.0)
    assert manager.state_time == 6.0
    job = manager.accepted_requests()[0][1]
    assert job.request == request
    assert job.is_running()
    assert job.mapping
    assert job.last_mapping
    assert job.cratio == 1.0 / (job_end_time - 5.0)
    assert manager.schedule.start_time == 6.0

    # add two new requests
    request = manager.new_request(graph, mappings, timeout=10.0)
    request = manager.new_request(graph, mappings, timeout=8.0)
    manager.generate_schedule()

    # Jump over one segment
    manager.advance_to_time(10.5)
    assert len(manager.schedule.segments()) == 2
    assert manager.schedule.start_time == 10.5

    request = manager.new_request(graph, mappings, timeout=5.5)
    manager.generate_schedule()
    segment_end_time = manager.schedule.segments()[0].end_time
    assert len(manager.accepted_requests()) == 3

    # Jump by a segment
    manager.advance_segment()
    assert manager.state_time == segment_end_time
    assert manager.schedule.start_time == segment_end_time
    assert len(manager.accepted_requests()) == 2

    # Jump after the schedule
    manager.advance_to_time(20.0)
    assert not manager.schedule
    assert manager.state_time == 20.0
    assert not manager.accepted_requests()


def test_manager_advance_to_time_raise(platform, graph, mappings):
    scheduler = MedfScheduler(platform)
    manager = ResourceManager(platform, scheduler)
    assert manager.state_time == 0.0

    # Advance the manager to the past
    with pytest.raises(RuntimeError):
        manager.advance_to_time(-5.0)

    manager.new_request(graph, mappings, timeout=10.0)

    # cannot advance with a new unscheduled request
    with pytest.raises(RuntimeError):
        manager.advance_to_time(1.0)

    schedule = manager.generate_schedule()

    # Manually remove schedule
    manager._schedule = None
    with pytest.raises(RuntimeError):
        manager.advance_to_time(1.0)

    manager._schedule = schedule
