# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import sys
import numpy as np
from hydra.utils import instantiate
from mocasin.representations import MappingRepresentation

import mocasin.util.random_distributions.lp as lp

from mocasin.util import logging

log = logging.getLogger(__name__)


class Volume(object):
    def __init__(self):
        log.debug("create default volume")

    def adapt(vol):
        log.debug("adapt volume")
        return vol

    def shrink(vol):
        log.debug("shrink volume")
        return vol


class Cube(Volume):
    def __init__(
        self,
        graph,
        platform,
        representation,
        center,
        radius=1.0,
        max_step=10,
        max_pe=16,
    ):
        # define initial cube with radius 1 at the given center
        self.center = center.to_list()
        self.radius = radius
        self.dim = len(center)
        # https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

    def adapt_center(self, s_set):
        fs_set = list(map(lambda s: s.sample, s_set.get_feasible()))
        if not fs_set:
            return self.center
        # take mean of feasible points as new center
        m = np.mean(fs_set, axis=0)
        self.center = np.around(m).tolist()
        return self.center

    def correct_center(self, s_set, center, old_center):
        # shortest points to center
        d_cur = list(map(lambda s: [s.dist(center), s], s_set.get_feasible()))
        d_cur = sorted(d_cur, key=lambda x: x[0])
        nearest_samples = []
        for s in d_cur:
            if s[0] == d_cur[0][0]:
                nearest_samples.append(s[1])
        # take (first) shortest point to old center from that result
        d_old = list(
            map(lambda s: [s.dist(old_center), s], s_set.get_feasible())
        )
        d_old = sorted(d_old, key=lambda x: x[0])
        for s in d_old:
            if s[1] in nearest_samples:
                return s[1].sample
        return None

    def adapt_volume(self, s_set, target_p, s_val):
        fs_set = list(map(lambda s: s.sample, s_set.get_feasible()))
        # adjust radius
        p = len(s_set.get_feasible()) / len(s_set.sample_set)
        log.debug("---------- adapt_volume() -----------")
        log.debug(
            "p-factors: {} {}".format(
                s_set.get_feasible(), len(s_set.sample_set)
            )
        )
        if p >= target_p:
            # simple adaptation: cube does not support shape adaption
            log.debug(
                "extend at p: {:f} target_p {:f} r: {:f}".format(
                    p, target_p, self.radius
                )
            )
            self.extend(s_val)
        else:
            log.debug(
                "shrink at p: {:f} target_p {:f} r: {:f}".format(
                    p, target_p, self.radius
                )
            )
            self.shrink(s_val)
        return p

    def shrink(self, step):
        # shink volume by one on each border
        self.radius = self.radius - 1 if (self.radius - 1 > 0) else self.radius

    def extend(self, step):
        # extend volume by one on each border
        self.radius = (
            self.radius + step * self.max_step
            if (self.radius + step * self.max_step < self.max_pe)
            else self.radius
        )


class LPVolume(Volume):
    def __init__(
        self,
        graph,
        platform,
        representation,
        center,
        radius,
        adaptable_center_weights=True,
        aggressive_center_movement=False,
        adapt_samples=0,
    ):
        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation, graph, platform)
        self.representation = representation
        self.graph = graph
        self.platform = platform
        self.adaptable_center_weights = adaptable_center_weights
        self.adapt_samples = adapt_samples
        self.aggressive_center_movement = aggressive_center_movement
        self.center = np.array(self.representation.toRepresentation(center))
        log.debug(f"Initializing center with representation:{self.center}")
        self.old_center = self.center
        self.radius = radius
        self.dim = len(self.center)
        self.true_dim = len(graph.processes())
        if not hasattr(self.representation, "p"):
            raise RuntimeError("Representation does not have a norm")
        self.norm_p = representation.p
        self.weight_center = 1 / (np.exp(1) * self.dim)
        self.rk1_learning_constant = 1 / np.sqrt(self.true_dim)
        self.rk1_vec = np.zeros(self.dim)
        self.transformation = np.identity(self.dim) * self.radius ** 2
        self.adapt_covariance()

    def update_factors(self, p, num_samples):
        self.learning_rate = 0.6 / (
            (self.true_dim + 1.3) ** 2 + p * num_samples
        )  # Beta
        self.expansion_factor = 1 + (self.learning_rate * (1 - p))  # f_e
        self.contraction_factor = 1 - (self.learning_rate * p)  # f_c

    def adapt_center(self, s_set):
        # all feas. samples in s_set
        fs_set = list(map(lambda s: s.sample, s_set.get_feasible()))
        if fs_set == []:
            return self.center
        # take mean of feasible points to add weighted to the old center
        num_feasible = len(fs_set)  # mu
        if self.adaptable_center_weights:
            self.weight_center = min(
                0.5, num_feasible / (np.exp(1) * self.true_dim)
            )
        if self.aggressive_center_movement:
            self.weight_center = 0.51

        mean_center = np.mean(fs_set, axis=0)
        mean_center_approx = self.representation.approximate(mean_center)
        log.debug("mean mapping {}".format(mean_center))
        new_center_vec = (
            1 - self.weight_center
        ) * self.center + self.weight_center * np.array(mean_center_approx)
        vector_of_distances = [
            lp.p_norm(self.center - v, self.norm_p) for v in fs_set
        ]
        if min(vector_of_distances) <= 0:
            log.warning("DC points did not move.")
        # approximate center
        new_center = self.representation.approximate(new_center_vec)
        dist1 = lp.p_norm(mean_center_approx - self.center, self.norm_p)
        if np.allclose(dist1, 0):
            log.warning("DC mean center unchanged.")
        else:
            log.info(f"DC mean center moved by {dist1}")
        self.old_center = self.center
        self.center = np.array(new_center)
        dist2 = lp.p_norm(self.old_center - self.center, self.norm_p)
        if np.allclose(dist2, 0):
            log.warning("DC Center unchanged.")
        else:
            log.info(f"DC center moved by {dist2}")
        return self.center

    def correct_center(self, s_set, center, old_center):
        log.error(
            "This function (correct_center) is deprecated and should not be called."
        )
        sys.exit(-1)

    def adapt_volume(self, s_set, target_p, s_val):
        fs_set = list(map(lambda s: s.sample, s_set.get_feasible()))
        # adjust radius
        num_feasible = len(s_set.get_feasible())
        num_samples = len(s_set.sample_set)
        assert num_samples <= self.adapt_samples or log.error(
            f"number of samples produced ({num_samples}) exceeds self.configuration ({self.adapt_samples})"
        )
        self.update_factors(target_p, num_samples)
        if num_feasible != 0:
            p_emp = num_feasible / num_samples
        else:
            p_emp = 0
        log.debug("---------- adapt_volume() -----------")
        self.adapt_radius(num_feasible, num_samples)
        self.adapt_transformation(s_set)
        return p_emp

    def adapt_radius(self, num_feasible, num_samples):
        factor = (
            self.expansion_factor ** num_feasible
            * self.contraction_factor ** (num_samples - num_feasible)
        )
        if factor > 1:
            log.debug(f"extend radius {self.radius} by factor: {factor}")
        else:
            log.debug(f"shrink radius {self.radius} by factor: {factor}")
        # print(f"radius: {self.radius} with p_emp = {num_feasible/num_samples} yields factor {factor}")
        self.radius = self.radius * factor

    def adapt_transformation(self, s_set):
        """
        This function adapts the transformation matrix of the ball around the center.
        It assumes it is called *after* adapt_center!
        """
        feasible = s_set.get_feasible()
        num_feasible = len(feasible)

        if num_feasible == 0:
            return

        centers = self.center - self.old_center
        centers_factor = np.sqrt(
            self.rk1_learning_constant * (2 - self.rk1_learning_constant)
        )
        self.rk1_vec = (1 - self.rk1_learning_constant) * self.rk1_vec
        if np.dot(centers, centers.transpose()) != 0:
            centers_alpha = 1 / np.sqrt(np.dot(centers, centers))
            self.rk1_vec += centers_factor * centers_alpha * centers
        rank_one_update = np.array(self.rk1_vec).transpose() @ np.array(
            self.rk1_vec
        )

        rank_mu_update = np.zeros([self.dim, self.dim])
        try:
            Qinv = np.linalg.inv(self.covariance)
        except np.linalg.LinAlgError:
            Qinv = np.identity(self.dim)
        arnorm = dict()
        for j, X in enumerate(feasible):
            V = Qinv @ (np.array(X.sample2tuple()) - self.old_center)
            # TODO: look up the alphas in original implementation, as not described in paper
            arnorm[j] = np.sqrt(np.dot(V, V))
            if arnorm[j] != 0:
                arnorm[j] = 1 / arnorm[j]
            else:
                arnorm[j] = 0

        for j, X in enumerate(feasible):
            alphai = np.sqrt(self.dim) * min(
                np.median(np.array(list(arnorm.values()))), 2.0 * arnorm[j]
            )

            rank_1_matrix = np.array(V).transpose() @ np.array(V)
            rank_mu_update += 1 / num_feasible * alphai * rank_1_matrix

        rk_1_weight = 0.6 / ((self.true_dim + 1.3) ** 2 + num_feasible)
        rk_mu_weight = (
            0.04
            * (num_feasible - 2 + (1 / num_feasible))
            / ((self.dim + 2) ** 2 + 0.2 * num_feasible)
        )

        self.transformation = (
            1 - rk_1_weight - rk_mu_weight
        ) * self.transformation
        self.transformation += rk_1_weight * rank_one_update
        self.transformation += rk_mu_weight * rank_mu_update
        self.adapt_covariance()

    def adapt_covariance(self):

        vals, vecs = np.linalg.eig(self.transformation)

        idx = (
            vals.argsort()
        )  # why would I sort them? #Josefine does in her matlab implementation...
        vals_sqrt_diag = np.sqrt(vals[idx])
        norm = np.prod(vals_sqrt_diag ** (1 / self.dim))
        vals_sqrt_diag = vals_sqrt_diag * 1 / norm
        Q = vecs[idx] * vals_sqrt_diag
        # Q @ Q.transpose() is approx. self.transformation (modulo norm)
        self.covariance = Q
        norm = np.abs(np.linalg.det(self.covariance))
        cnt = 0
        while not np.allclose(norm, 1, atol=0.1 ** (11 - cnt)) and cnt < 10:
            log.warning(f"covariance matrix not normed ({norm}), retrying.")
            norm = np.abs(np.linalg.det(self.covariance))
            cnt += 1
            self.covariance = np.real(
                1 / (norm ** (1 / self.dim)) * self.covariance
            )
        if not np.allclose(norm, 1, atol=0.1 ** (11 - cnt)):
            log.warning(
                f"failed to norm ({norm}) covariance matrix. Resetting to identity"
            )
            self.transformation = np.identity(self.dim) * self.radius ** 2
            self.covariance = np.identity(self.dim)

    # def draw_volume_projection(self,coordinates):
    #    assert(len(coordinates) == 2)
