# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import traceback
import pint
from sys import exit

from copy import deepcopy
from mocasin.mapper.partial import ProcPartialMapper, ComPartialMapper
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper import utils
from mocasin.simulate import KpnSimulation


from mocasin.util import logging

log = logging.getLogger(__name__)


class Oracle(object):
    def __init__(
        self,
        oracle_type,
        kpn,
        platform,
        trace_generator,
        threshold,
        threads=None,
    ):

        self.oracle_type = oracle_type

        if oracle_type == "TestSet":
            self.oracle = TestSet()
        elif oracle_type == "TestTwoPrKPN":
            self.oracle = TestTwoPrKPN()
        elif oracle_type == "simulation":
            self.oracle = Simulation(
                kpn, platform, trace_generator, threshold, threads=1
            )
        else:
            log.error("Error, unknown oracle:" + oracle_type)
            exit(1)

    def validate(self, sample):
        """ check whether a single sample is feasible """
        res = self.oracle.is_feasible(sample.sample2simpleTuple)
        return res

    def validate_set(self, samples):
        """ check whether a set of samples is feasible """
        # extra switch for evaluation of static sets vs. simulation
        res = []
        self.prepare_sim_contexts_for_samples(samples)

        for s in samples:
            mapping = tuple(s.getMapping().to_list())
            if mapping in self.cache:
                log.debug(f"skipping simulation for mapping {mapping}: cached.")
                s.sim_context.exec_time = self.cache[mapping]

        if self.oracle_type != "simulation":
            for s in samples:
                res.append(self.is_feasible(s.sample2simpleTuple))
        else:
            res = self.is_feasible(samples)

        return res


class Simulation(Oracle):
    """ simulation code """

    def __init__(self, kpn, platform, trace_generator, threshold, threads=1):
        self.kpn = kpn
        self.platform = platform
        self.trace_generator = trace_generator
        self.randMapGen = RandomPartialMapper(self.kpn, self.platform)
        self.comMapGen = ComPartialMapper(
            self.kpn, self.platform, self.randMapGen
        )
        self.dcMapGen = ProcPartialMapper(
            self.kpn, self.platform, self.comMapGen
        )
        self.threads = threads
        self.threshold = threshold
        self.cache = {}
        self.total_cached = 0
        self.oracle_type = "simulation"

    def prepare_sim_contexts_for_samples(self, samples):
        """ Prepare simualtion/application context and mapping for a each element in `samples`. """

        # Create a list of 'simulation contexts'.
        # These can be later executed by multiple worker processes.
        simulation_contexts = []

        for i in range(0, len(samples)):
            log.debug("Using simcontext no.: {} {}".format(i, samples[i]))
            # create a simulation context
            mapping = self.dcMapGen.generate_mapping(
                list(map(int, samples[i].sample2simpleTuple()))
            )
            sim_context = self.prepare_sim_context(mapping)
            samples[i].setSimContext(sim_context)

    def prepare_sim_context(self, mapping):
        sim_mapping = self.dcMapGen.generate_mapping(mapping.to_list())
        self.trace_generator.reset()
        trace = deepcopy(self.trace_generator)
        sim_context = KpnSimulation(self.platform, self.kpn, sim_mapping, trace)
        log.debug("Mapping toList: {}".format(sim_mapping.to_list()))
        return sim_context

    def is_feasible(self, samples):
        """Checks if a set of samples is feasible in context of a given timing threshold.

        Trigger the simulation on 4 for parallel jobs and process the resulting array
        of simulation results according to the given threshold.
        """
        results = []
        # run simulations and search for the best mapping
        if len(samples) > 1 and self.threads > 1:
            # run parallel simulation for more than one sample in samples list
            from multiprocessing import Pool

            log.debug(
                "Running parallel simulation for {} samples".format(
                    len(samples)
                )
            )
            pool = Pool(processes=self.threads, maxtasksperchild=100)
            results = list(
                pool.map(self.run_simulation, samples, chunksize=self.threads)
            )
        else:
            # results list of simulation contexts
            log.debug("Running single simulation")
            results = list(map(self.run_simulation, samples))

        # find runtime from results
        exec_times = []  # in ps
        for r in results:
            exec_times.append(float(r.sim_context.exec_time))

        feasible = []
        for r in results:
            assert r.sim_context.exec_time is not None
            ureg = pint.UnitRegistry()
            threshold = ureg(self.threshold).to(ureg.ps).magnitude

            if r.sim_context.exec_time > threshold:
                r.setFeasibility(False)
                feasible.append(False)
            else:
                r.setFeasibility(True)
                feasible.append(True)

        log.debug("Exec.-Times: {} Feasible: {}".format(exec_times, feasible))
        # return samples with the according sim context
        return results

    def run_simulation(self, sample):
        # do simulation requires sim_context
        if sample.sim_context.exec_time is not None:
            self.total_cached += 1
            return sample
        try:
            utils.run_simulation(sample.sim_context)

            # add to cache
            mapping = tuple(sample.getMapping().to_list())
            self.cache[mapping] = sample.sim_context.exec_time

        except Exception as e:
            log.debug("Exception in Simulation: {}".format(str(e)))
            traceback.print_exc()
            # log.exception(str(e))
            if hasattr(e, "details"):
                log.info(e.details())
        return sample


# This is a temporary test class
class TestSet(Oracle):
    # specify a fesability test set
    def is_feasible(self, s):
        """ test oracle function (2-dim) """
        # print("oracle for: " + str(s))
        if len(s) != 2:
            log.error("test oracle requires a dimension of 2\n")
            exit(1)
        x = s[0]
        y = s[1]
        if (x in range(1, 3)) and (y in range(1, 3)):  # 1<=x<=2 1<=y<=2
            return True
        if (x in range(1, 4)) and (y in range(13, 15)):
            return True
        if (x in range(9, 11)) and (y in range(9, 11)):
            return False
        if (x in range(7, 13)) and (y in range(7, 13)):
            return True
        else:
            return False


class TestTwoPrKPN(Oracle):
    def is_feasible(self, s):
        """ test oracle function (2-dim) """
        if len(s) != 2:
            log.error("test oracle requires a dimension of 2\n")
            exit(1)
        x = s[0]
        y = s[1]
        if x == y:  # same PE
            return False
        elif x < 0 or x > 15 or y < 0 or y > 15:  # outside of area
            # print("outside area")
            return False
        elif divmod(x, 4)[0] == divmod(y, 4)[0]:  # same cluster
            return True
        else:
            return False
