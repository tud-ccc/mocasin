# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from collections import Counter
import copy
from enum import Flag, auto
import logging
import math
import random

log = logging.getLogger(__name__)


class LRConstraint(Flag):
    NULL = 0
    RESOURCE = auto()
    DELAY = auto()
    RDP = auto()


class LRSolver:
    """Lagrangian relaxation solver.

    Lagrangian function is
    Lagr(x,lambda) = sum_{i=1}^n (e(x_i) + sum_{k=1}^m lambda_k*(r_k(x_i)-R_k))

    Dual function is
    g(lambda) = min_x Lagr(x,lambda)
              = sum_{i=1}^n min_{x_i} {e(x_i) + sum_{k=1}^m lambda_k*r_k(x_i) }
                - sum_{k=1}^m lambda_k*R_k
              = sum_{i=1}^n min_{x_i} f(x_i, lambda) - sum_{k=1}^m lambda_k*R_k

    Dual optimization problem:
        maximize g(lambda)
        subject to lambda >= 0

    The solution is denoted by lambda*.
    The selected operating points are x_i^* = argmax_{x_i} f(x_i, lambda*)

    The problem is solved by decomposition into a master problem and several
    subproblems by applying a subgradient method.

    Stefan Wildermann, Michael Glaß, and Jürgen Teich. 2014. Multi-objective
    distributed run-time resource management for many-cores. In Proceedings of
    the conference on Design, Automation & Test in Europe (DATE '14).
    """
    def __init__(self, platform, constraints=LRConstraint.RESOURCE,
                 rounds=1000, params=None):
        assert isinstance(constraints, LRConstraint)
        self.platform = platform

        if params is None:
            # Use default values
            params = LRSolver.default_params()

        self.__relax_r = bool(constraints & LRConstraint.RESOURCE)
        self.__relax_d = bool(constraints & LRConstraint.DELAY)
        self.__relax_rdp = bool(constraints & LRConstraint.RDP)

        # Extract value from params
        self.__max_rounds = rounds
        self.__step_size_resource = params['step_size_resource']
        self.__step_size_delay = params['step_size_delay']
        self.__step_size_rdp = params['step_size_rdp']

        self.__verbose = True

    @staticmethod
    def default_params():
        """Generate default solver parameters."""
        res = {}
        res['step_size_resource'] = lambda x: 0.1 / math.sqrt(x)
        res['step_size_delay'] = lambda x: 0.001 / math.sqrt(x)
        res['step_size_rdp'] = lambda x: 0.001 / math.sqrt(x)
        return res

    @staticmethod
    def _job_config_energy(job, mapping):
        return mapping.metadata.energy * (1.0 - job.cratio)

    @staticmethod
    def _job_config_delay(job, mapping):
        return mapping.metadata.exec_time * (1.0 - job.cratio)

    @staticmethod
    def _job_config_resource(job, mapping):
        return mapping.get_used_processor_types()

    @staticmethod
    def _job_config_rdp(job, mapping):
        return Counter({
            k: v * mapping.metadata.exec_time * (1.0 - job.cratio)
            for k, v in mapping.get_used_processor_types().items()
        })

    @staticmethod
    def job_config_cost(job, mapping, l):
        """Calculates

        f(x_i, (lambda_d_i, lambda_r, lambda_rdp)) =
            e(x_i) + lambda_d_i * t(x_i) +
            sum_{k=1..m} lambda_r_k * r_k(x_i) +
            sum_{k=1..m} lambda_rdp_k * t(x_i) * r_k(x_i)

        Args:
            job (Job): A job
            config (CanonicalMapping): A canonical mapping.
            l (tuple): Lambda

        Returns the result of function
        """
        assert isinstance(l, tuple)
        cratio = job.cratio
        l_d, l_r, l_rdp = l

        # e(x_i)
        res = LRSolver._job_config_energy(job, mapping)
        # lambda_d_i * t(x_i)
        if l_d is not None:
            res += l_d[job.request] * LRSolver._job_config_delay(job, mapping)
        if l_r is not None:
            m_r = LRSolver._job_config_resource(job, mapping)
            res += sum(
                Counter({k: l_r[k] * m_r[k]
                         for k in l_r.keys() & m_r}).values())
        if l_rdp is not None:
            m_rdp = LRSolver._job_config_rdp(job, mapping)
            res += sum(
                Counter({k: l_rdp[k] * m_rdp[k]
                         for k in l_rdp.keys() & m_rdp}).values())
        return res

    @staticmethod
    def _job_min_cost(job, l):
        """Find min_{x_i} f(x_i, lambda).

        Returns min_config_name, config, f(min_config, lambda).
        """
        assert isinstance(l, tuple)
        cratio = job.cratio

        configs = [(LRSolver.job_config_cost(job, mapping, l), mapping)
                   for mapping in job.request.mappings]
        min_cost, min_mapping = min(configs, key=lambda x: x[0])
        return min_mapping, min_cost

    def __initial_lambda(self, jobs):
        """Initiate lambda for all types of constraints.

        Returns:
            A tuple (lambda_d, lambda_r, lambda_rdp)"""
        l_r = None
        l_rdp = None
        l_d = None
        if self.__relax_r:
            l_r = Counter()
        if self.__relax_rdp:
            l_rdp = Counter()
        if self.__relax_d:
            l_d = {j.request: random.random() * 10 for j in jobs}
        return tuple((l_d, l_r, l_rdp))

    def __log_lambda(self, l):
        l_d, l_r, l_rdp = l
        if self.__relax_d:
            log.debug("lamda_d: {} ".format(l_d))
        if self.__relax_r:
            log.debug("lamda_r: {} ".format(l_r))
        if self.__relax_rdp:
            log.debug("lamda_rdp: {} ".format(l_rdp))

    def solve(self, jobs, segment_start_time=0.0):
        """Run the solver."""
        # Initial values
        l = self.__initial_lambda(jobs)

        if self.__relax_rdp:
            window = max([
                job.deadline - segment_start_time
                for job in jobs if job.deadline != math.inf
            ], default=math.inf)
            # assert window != math.inf, "NYI"

        for t in range(1, self.__max_rounds + 1):
            if self.__verbose:
                log.debug("Round: {}".format(t))
                self.__log_lambda(l)

            # Copy l
            new_l_d, new_l_r, new_l_rdp = copy.copy(l)
            changed = False

            # Initiate results for found job configs
            # [(job, config_name, config)]
            # TODO: Remove explicit config_name
            min_configs = []

            for job in jobs:
                # Application subproblem
                job_mapping, job_cost = LRSolver._job_min_cost(job, l)
                min_configs.append(tuple((job, job_mapping)))
                if self.__verbose:
                    log.debug("Job {}, mapping = {}, time = {}, energy = {}"
                              " deadline = {}, f = {}".format(
                                  job.to_str(),
                                  job_mapping.get_used_processor_types(),
                                  job_mapping.metadata.exec_time *
                                  (1.0 - job.cratio),
                                  job_mapping.metadata.energy *
                                  (1.0 - job.cratio), job.deadline, job_cost))
                # Calculate subgradient of delay coefficients
                if self.__relax_d:
                    if job.deadline == math.inf:
                        assert False, "NYI"
                        new_l_d[job.rid] = 0.0
                    else:
                        delta = LRSolver._job_config_delay(
                            job, job_mapping) - job.deadline
                        new_l_d[job.request] = max(
                            0.0, (l[0][job.request] +
                                  delta * self.__step_size_delay(t)))
                    if new_l_d[job.request] != l[0][job.request]:
                        changed = True

            # Calculate subgradient of resource coefficients
            if self.__relax_r:
                delta = sum([
                    LRSolver._job_config_resource(job, mapping)
                    for job, mapping in min_configs
                ], Counter())
                delta.subtract(self.platform.get_processor_types())
                #print(l[1])
                new_l_r = (Counter({
                    k: l[1][k] + delta[k] * self.__step_size_resource(t)
                    for k in self.platform.get_processor_types()
                }) | Counter())
                #print(new_l_r)
                if l[1] != new_l_r:
                    changed = True

            # Calculate subgradient of rdp coefficients
            if self.__relax_rdp:
                delta = sum([
                    LRSolver._job_config_rdp(job, mapping)
                    for job, mapping in min_configs if job.deadline != math.inf
                ], Counter())
                delta.subtract(
                    Counter({
                        k: v * window
                        for k, v in
                        self.platform.get_processor_types().items()
                    }))
                new_l_rdp = (Counter({
                    k: l[2][k] + delta[k] * self.__step_size_rdp(t)
                    for k in self.platform.get_processor_types()
                }) | Counter())
                if l[2] != new_l_rdp:
                    changed = True

            if not changed:
                if self.__verbose:
                    log.debug("New lambda value is the same as previous."
                              " Stopping iterating.")
                break
            l = tuple((new_l_d, new_l_r, new_l_rdp))

        log.debug("Returned the following lambda coefficients:")
        self.__log_lambda(l)
        return l, min_configs
