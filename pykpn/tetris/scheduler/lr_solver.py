from pykpn.common.platform import Platform
from pykpn.tetris.job import Job, JobTable
from pykpn.tetris.extra import NamedDimensionalNumber
from pykpn.tetris.apptable import CanonicalMapping

import logging
log = logging.getLogger(__name__)

from enum import Flag, auto
import math
import copy
import random


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
        assert isinstance(platform, Platform)
        assert isinstance(constraints, LRConstraint)
        self.__platform = platform

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
    def __job_config_energy(job, config):
        return config.energy(start_cratio=job.cratio)

    @staticmethod
    def __job_config_delay(job, config):
        return config.time(start_cratio=job.cratio)

    @staticmethod
    def __job_config_resource(job, config):
        return config.core_types

    @staticmethod
    def __job_config_rdp(job, config):
        return config.core_types * config.time(start_cratio=job.cratio)

    @staticmethod
    def job_config_cost(job, config, l):
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
        assert isinstance(job, Job)
        assert isinstance(config, CanonicalMapping), (
            "Config must be a type of CanonicalMapping, but it is {}".format(
                type(config)))
        assert isinstance(l, tuple)
        # No idle mappings
        assert config.time != math.inf

        cratio = job.cratio
        rid = job.rid
        l_d, l_r, l_rdp = l

        # e(x_i)
        res = LRSolver.__job_config_energy(job, config)
        # lambda_d_i * t(x_i)
        if l_d is not None:
            res += l_d[rid] * LRSolver.__job_config_delay(job, config)
        if l_r is not None:
            res += (l_r * LRSolver.__job_config_resource(
                job, config)).reduce(lambda x, y: x + y)
        if l_rdp is not None:
            res += (l_rdp * LRSolver.__job_config_rdp(
                job, config)).reduce(lambda x, y: x + y)
        return res

    @staticmethod
    def __job_min_cost(job, l):
        """Find min_{x_i} f(x_i, lambda).

        Returns min_config_name, config, f(min_config, lambda).
        """
        assert isinstance(job, Job)
        assert isinstance(l, tuple)
        cratio = job.cratio

        configs = [(name, can_mapping,
                    LRSolver.job_config_cost(job, can_mapping, l))
                   for name, can_mapping in job.app.mappings.items()
                   if name != "__idle__"]
        min_name, min_config, min_cost = min(configs, key=lambda x: x[2])

        return min_name, min_config, min_cost

    def __initial_lambda(self, jobs):
        """Initiate lambda for all types of constraints.

        Returns:
            A tuple (lambda_d, lambda_r, lambda_rdp)"""
        l_r = None
        l_rdp = None
        l_d = None
        if self.__relax_r:
            l_r = NamedDimensionalNumber(self.__platform.core_types(),
                                         init_only_names=True)
        if self.__relax_rdp:
            l_rdp = NamedDimensionalNumber(self.__platform.core_types(),
                                           init_only_names=True)
        if self.__relax_d:
            l_d = {}
            for j in jobs:
                l_d[j.rid] = random.random() * 10
        return tuple((l_d, l_r, l_rdp))

    def __log_lambda(self, l):
        l_d, l_r, l_rdp = l
        if self.__relax_d:
            log.debug("lamda_d: {} ".format(l_d))
        if self.__relax_r:
            log.debug("lamda_r: {} ".format(l_r))
        if self.__relax_rdp:
            log.debug("lamda_rdp: {} ".format(l_rdp))

    def solve(self, jobs):
        """Run the solver."""
        assert isinstance(jobs, JobTable)

        # Initial values
        l = self.__initial_lambda(jobs)

        if self.__relax_rdp:
            window = max(
                [job.deadline for job in jobs if job.deadline != math.inf],
                default=math.inf)
            # assert window != math.inf, "NYI"

        for t in range(1, self.__max_rounds + 1):
            if self.__verbose:
                log.debug("Round: {}".format(t))
                self.__log_lambda(l)

            # Copy l
            new_l_d, new_l_r, new_l_rdp = copy.deepcopy(l)
            changed = False

            # Initiate results for found job configs
            # [(job, config_name, config)]
            # TODO: Remove explicit config_name
            min_configs = []

            for job in jobs:
                # Application subproblem
                job_config_name, job_config, min_cost = LRSolver.__job_min_cost(
                    job, l)
                min_configs.append(tuple((job, job_config_name, job_config)))
                if self.__verbose:
                    log.debug("Job rid = {}, config = {}[{}], time = {},"
                              " deadline = {}, f = {}".format(
                                  job.rid, job_config_name,
                                  job_config.core_types,
                                  job_config.time(start_cratio=job.cratio),
                                  job.deadline, min_cost))
                # Calculate subgradient of delay coefficients
                if self.__relax_d:
                    if job.deadline == math.inf:
                        new_l_d[job.rid] = 0.0
                    else:
                        delta = LRSolver.__job_config_delay(
                            job, job_config) - job.deadline
                        new_l_d[job.rid] = max(
                            0.0, (l[0][job.rid] +
                                  delta * self.__step_size_delay(t)))
                    if new_l_d[job.rid] != l[0][job.rid]:
                        changed = True

            # Calculate subgradient of resource coefficients
            if self.__relax_r:
                delta = (sum(
                    [
                        LRSolver.__job_config_resource(job, config)
                        for job, _, config in min_configs
                    ],
                    NamedDimensionalNumber(
                        self.__platform.core_types(),
                        init_only_names=True))) - NamedDimensionalNumber(
                            self.__platform.core_types())
                new_l_r = NamedDimensionalNumber.max_per_dim(
                    l[1] + delta * self.__step_size_resource(t), 0.0)
                if l[1] != new_l_r:
                    changed = True

            # Calculate subgradient of rdp coefficients
            if self.__relax_rdp:
                delta = sum(
                    [
                        LRSolver.__job_config_rdp(job, config)
                        for job, _, config in min_configs
                        if job.deadline != math.inf
                    ],
                    NamedDimensionalNumber(
                        self.__platform.core_types(),
                        init_only_names=True)) - (NamedDimensionalNumber(
                            self.__platform.core_types()) * window)
                new_l_rdp = NamedDimensionalNumber.max_per_dim(
                    l[2] + delta * self.__step_size_rdp(t), 0.0)
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
