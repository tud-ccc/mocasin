# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Andrés Goens

from itertools import chain, combinations
import hydra
from pathlib import Path
import pickle
import sys

from pykpn.util import logging
from pykpn.mapper.genetic import GeneticMapper
from pykpn.mapper.from_file import FromFileMapper
from pykpn.representations import SymmetryRepresentation

from pykpn.tetris.job_request import JobRequestInfo
from pykpn.tetris.job_state import Job

log = logging.getLogger(__name__)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class TetrisMapper(object):
    def __init__(self, platform, scheduler, pareto_dir="pareto_mappings/"):
        """Generates a full mapping for a given platform and KPN application.

        :param platform: a platform
        :type platform: Platform
        """
        self.platform = platform
        self.pareto_dir = pareto_dir
        self.scheduler = scheduler

        log.info(f"Scheduler {self.scheduler.name} "
                 f"rotations={self.scheduler.rotations} "
                 f"migrations={self.scheduler.migrations} "
                 f"preemptions={self.scheduler.preemptions}")

    @staticmethod
    def from_hydra(platform, cfg):
        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg['resource_manager'], platform)
        mapper = TetrisMapper(platform, scheduler, cfg['pareto_dir'])
        return mapper

    def generate_pareto_fronts(self, kpns, traces):
        pareto_dir = self.pareto_dir
        pareto_fronts = {}
        pareto_path = Path(pareto_dir)
        pareto_path.mkdir(parents=True, exist_ok=True)
        log.info("Generating Pareto-optimal solutions")
        for kpn, trace in zip(kpns, traces):
            representation = SymmetryRepresentation(kpn, self.platform)
            gen_mapper = GeneticMapper(kpn, self.platform, trace,
                                       representation,
                                       objective_exec_time=True,
                                       objective_num_resources=True,
                                       record_statistics=False)
            kpn_path = pareto_path.joinpath(kpn.name)
            kpn_path.mkdir(exist_ok=True)
            if len(list(kpn_path.glob(f"mapping_*.pickle"))) == 0:
                log.info(f"Pareto points for {kpn.name} not found. "
                         "Generating... ")
                par_mappings = gen_mapper.generate_pareto_front()
                sys.setrecursionlimit(2000)
                for j, point in enumerate(par_mappings):
                    mapping_path = kpn_path.joinpath(f"mapping_{j}.pickle")
                    with open(mapping_path, 'wb') as f:
                        p = pickle.Pickler(f)
                        p.dump(point)
            else:
                mapper = FromFileMapper(
                    kpn, self.platform, trace, representation,
                    files_pattern=f"{pareto_dir}/{kpn.name}/mapping_*.pickle")
                par_mappings = mapper.generate_multiple_mappings()
                log.info(f"Pareto points for {kpn.name} read from file")

            log.info(f"App({kpn.name}) has {len(par_mappings)} pareto points.")
            for i in range(len(par_mappings)):
                if par_mappings[i].metadata.energy is None:
                    #log.warning("The mapping has no energy value, "
                    #            "approximated it")
                    cnt = par_mappings[i].get_used_processor_types()
                    par_mappings[i].metadata.energy = (
                        par_mappings[i].metadata.exec_time *
                        (cnt['ARM_CORTEX_A7'] * 0.192 +
                         cnt['ARM_CORTEX_A15'] * 1.260))
                m = par_mappings[i]
                log.debug(f"Mapping: {m.get_used_processor_types()} "
                          f"exec_time: {m.metadata.exec_time}, "
                          f"energy: {m.metadata.energy}")
            pareto_fronts.update({kpn: par_mappings})
        return pareto_fronts

    def generate_mappings(self, kpns, traces):
        if len(kpns) == 0:
            return []
        log.info(f"Constructing mappings for {len(kpns)} apps with Tetris")
        if len(traces) != len(kpns):
            raise RuntimeError(
                f"Mapper received unbalanced number of traces ({len(traces)}) "
                f"and applications ({len(kpns)})")

        # Generate pareto-fronts
        pareto_fronts = self.generate_pareto_fronts(kpns, traces)

        # Prepare job requests
        job_requests = []
        for kpn, mappings in pareto_fronts.items():
            job_requests.append(
                JobRequestInfo(kpn, mappings, 0.0, deadline=2.5))
        jobs = list(
            map(lambda x: x.dispatch(), Job.from_requests(job_requests)))

        log.info("Running Tetris scheduler")
        schedule = None
        for cjobs in reversed(list(powerset(jobs))):
            if len(cjobs) == 0:
                continue
            schedule = self.scheduler.schedule(list(cjobs))
            if schedule is not None:
                break
        if schedule is None:
            log.info(f"Could not schedule any jobs")
            return [None] * len(jobs)
        log.info(f"Generated schedule: {schedule.to_str(verbose=True)}")
        job_mappings = schedule.get_job_mappings()
        res = []
        for kpn in kpns:
            job = next((job for job in job_mappings if job.app == kpn), None)
            if job is None:
                res.append(None)
            else:
                mappings = job_mappings.get(job, [None])
                assert len(mappings) == 1
                res.append(mappings[0])
        return res
