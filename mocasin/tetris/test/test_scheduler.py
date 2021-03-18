# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.tetris.job_request import JobRequestInfo
from mocasin.tetris.job_state import Job
from mocasin.tetris.scheduler.medf import MedfScheduler


def test_scheduler(platform, graph, pareto_mappings):
    request = JobRequestInfo(graph, pareto_mappings, arrival=0.0, deadline=10.0)
    job = Job.from_request(request)
    scheduler = MedfScheduler(platform)
    schedule = scheduler.schedule([job])
    assert len(schedule) == 1
    segment = schedule.first
    assert segment.start_time == 0.0
    assert segment.end_time == 9.7
    assert len(segment.jobs()) == 1
    assert segment.energy == 23.45
