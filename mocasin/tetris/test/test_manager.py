# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import pytest

from mocasin.tetris.job_request import JobRequestInfo, JobRequestStatus
from mocasin.tetris.manager_new import ResourceManager
from mocasin.tetris.scheduler.medf import MedfScheduler


def test_manager_new_request(platform, graph, mappings):
    scheduler = MedfScheduler(platform)
    manager = ResourceManager(platform, scheduler)

    assert manager.state_time == 0.0
    assert manager.schedule is None
    assert not manager.requests

    for i in range(1, 7):
        request = JobRequestInfo(graph, mappings, arrival=0.0, deadline=10.0)
        res = manager.new_request(request)
        assert res
        assert request.status == JobRequestStatus.ACCEPTED
        assert len(manager.requests) == i
        assert len(manager.accepted_requests()) == i
        assert len(manager.schedule.get_job_mappings()) == i
        assert manager.schedule.start_time == 0.0
        assert manager.schedule.end_time <= 10.0

    request = JobRequestInfo(graph, mappings, arrival=0.0, deadline=10.0)
    res = manager.new_request(request)
    assert not res
    assert request.status == JobRequestStatus.REFUSED
    assert len(manager.requests) == 7
    assert len(manager.accepted_requests()) == 6
    assert len(manager.schedule.get_job_mappings()) == 6
    assert manager.schedule.start_time == 0.0
    assert manager.schedule.end_time <= 10.0


def test_manager_new_request_raise(mocker):
    manager = ResourceManager(mocker.Mock(), mocker.Mock())

    # Only "new" reqeusts are accepted
    with pytest.raises(RuntimeError):
        request = JobRequestInfo(mocker.Mock(), mocker.Mock(), mocker.Mock())
        request.status = JobRequestStatus.ARRIVED
        manager.new_request(request)

    request = JobRequestInfo(mocker.Mock(), mocker.Mock(), mocker.Mock())
    manager.new_request(request)
    # Request cannot be added twice
    with pytest.raises(RuntimeError):
        manager.new_request(request)


def test_manager_advance_to_time(platform, graph, mappings):
    scheduler = MedfScheduler(platform)
    manager = ResourceManager(platform, scheduler)
    assert manager.state_time == 0.0

    # Advance the manager when it is free
    manager.advance_to_time(5.0)
    assert manager.state_time == 5.0

    # Add a request, check that the schedule's start time is 5.0
    request = JobRequestInfo(graph, mappings, arrival=5.0, deadline=10.0)
    res = manager.new_request(request)
    assert res
    assert manager.schedule.start_time == 5.0
    job_end_time = manager.schedule.end_time
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
    request = JobRequestInfo(graph, mappings, arrival=6.0, deadline=16.0)
    res = manager.new_request(request)
    assert res

    request = JobRequestInfo(graph, mappings, arrival=6.0, deadline=14.0)
    res = manager.new_request(request)

    # Jump over one segment
    manager.advance_to_time(10.5)
    assert len(manager.schedule) == 2
    assert manager.schedule.start_time == 10.5

    request = JobRequestInfo(graph, mappings, arrival=10.5, deadline=16.0)
    res = manager.new_request(request)
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

    request = JobRequestInfo(graph, mappings, arrival=0.0, deadline=10.0)
    res = manager.new_request(request)

    # Manually remove schedule
    schedule = manager.schedule
    manager.schedule = None
    with pytest.raises(RuntimeError):
        manager.advance_to_time(1.0)

    manager.schedule = schedule
