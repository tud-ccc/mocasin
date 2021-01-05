# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Andrés Goens

from os import mkdir
from os.path import isdir
from glob import glob
import pickle

from pykpn.util import logging
from pykpn.mapper.genetic import GeneticMapper
from pykpn.mapper.from_file import FromFileMapper
from pykpn.representations import SymmetryRepresentation

from pykpn.tetris.job_request import JobRequestInfo
from pykpn.tetris.job_state import Job
from pykpn.tetris.scheduler.dac import DacScheduler

log = logging.getLogger(__name__)


class TetrisMapper(object):
    def __init__(self, platform, pareto_dir = "pareto_mappings/"):
        """Generates a full mapping for a given platform and KPN application.

        :param platform: a platform
        :type platform: Platform
        """
        self.platform = platform

    def generate_mappings(self, kpns, traces, load=None, restricted=None):
        pareto_dir = self.pareto_dir
        if len(kpns) == 0:
            return []
        log.info(f"generating fair mapping for {len(kpns)} apps")

        if len(traces) != len(kpns):
            raise RuntimeError(
                f"Mapper received unbalanced number of traces ({len(traces)}) "
                f"and applications ({len(kpns)})")

        # Generate pareto-fronts
        pareto_fronts = {}
        mappings = {}
        if not isdir(f"{pareto_dir}"):
            mkdir(f"{pareto_dir}")
        for kpn, trace in zip(kpns, traces):
            representation = SymmetryRepresentation(kpn, self.platform)

            gen_mapper = GeneticMapper(kpn, self.platform, trace, representation,
                                       objective_exec_time=True, objective_num_resources=True,
                                       record_statistics=False)
            if not isdir(f"{pareto_dir}/{kpn.name}"):
                mkdir(f"{pareto_dir}/{kpn.name}")
            if len(glob(f"{pareto_dir}/{kpn.name}/mapping_*.pickle")) == 0:
                log.info(f"Pareto points for {kpn.name} not found. Generating... ")
                par_mappings = gen_mapper.generate_pareto_front()
                for j,point in enumerate(par_mappings):
                    with open(f"{pareto_dir}/{kpn.name}/mapping_{j}.pickle", 'wb') as f:
                        p = pickle.Pickler(f)
                        p.dump(point)
            else:
                mapper = FromFileMapper(kpn, self.platform, trace, representation,
                                        files_pattern=f"{pareto_dir}/{kpn.name}/mapping_*.pickle")
                par_mappings = mapper.generate_multiple_mappings()
                log.info(f"Pareto points for {kpn.name} read from file")

            log.info(f"App({kpn.name}) has {len(par_mappings)} pareto points.")
            for i in range(len(par_mappings)):
                if par_mappings[i].metadata.energy is None:
                    log.warning(
                        "The mapping has no energy value, set to execution time"
                    )
                    par_mappings[i].metadata.energy = par_mappings[i].metadata.exec_time
                m = par_mappings[i]
                print("Mapping: {}, exec_time: {}, energy: {}".format(
                    gen_mapper.evaluate_mapping(
                        gen_mapper.representation.toRepresentation(m)),
                    m.metadata.exec_time, m.metadata.energy))
            pareto_fronts.update({kpn: par_mappings})

        # Prepare job requests
        job_requests = []
        for kpn, mappings in pareto_fronts.items():
            job_requests.append(JobRequestInfo(kpn, mappings, 0.0))
        jobs = list(
            map(lambda x: x.dispatch(), Job.from_requests(job_requests)))

        scheduler = DacScheduler(self.platform, rotations = True)
        schedule = scheduler.schedule(jobs)
        print(schedule.to_str())
        job_mappings = schedule.get_job_mappings()
        res = []
        for kpn in kpns:
            job = next(job for job in job_mappings if job.app == kpn)
            mappings = job_mappings[job]
            assert len(mappings) == 1
            res.append(mappings[0])
        return res
