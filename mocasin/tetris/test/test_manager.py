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
        assert len(manager.schedule.get_job_mappings()) == i
        assert len(manager.requests) == i

    request = JobRequestInfo(graph, mappings, arrival=0.0, deadline=10.0)
    res = manager.new_request(request)
    assert not res
    assert request.status == JobRequestStatus.REFUSED
    assert len(manager.schedule.get_job_mappings()) == 6
    assert len(manager.requests) == 7


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
