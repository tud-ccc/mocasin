# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import hydra
import logging
import simpy
import timeit

from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem

log = logging.getLogger(__name__)


def kpn_to_dot(cfg):
    """Generate a dot graph from a KPN

    This simple task produces a dot graph that visualizes a given KPN. It
    expects two hydra parameters to be available.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **kpn:** the input kpn graph. The task expects a configuration dict that
          can be instantiated to a :class:`~pykpn.common.kpn.KpnGraph` object.
        * **dot:** the output file
    """
    kpn = hydra.utils.instantiate(cfg['kpn'])
    kpn.to_pydot().write_raw(cfg['dot'])


def platform_to_dot(cfg):
    """Generate a dot graph from a Platform

    This simple task produces a dot graph that visualizes a given Platform. It
    expects two hydra parameters to be available.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        * **dot:** the output file
    """
    platform = hydra.utils.instantiate(cfg['platform'])
    platform.to_pydot().write_raw(cfg['dot'])


def mapping_to_dot(cfg):
    """Generate a dot graph representing the mapping of a KPN application to a
    platform

    This task expects four hydra parameters to be available.

    **Hydra Parameters**:
        * **kpn:** the input kpn graph. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.kpn.KpnGraph`
          object.
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        * **mapping:** the input mapping. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.mapping.Mapping`
          object.
        * **dot:** the output file
    """
    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    mapping = hydra.utils.instantiate(cfg['mapping'], kpn, platform)
    mapping.to_pydot().write_raw(cfg['dot'])


def simulate(cfg):
    """Simulate the execution of a KPN application mapped to a platform.

    This script expects a configuration file as the first positional argument.
    It constructs a system according to this configuration and simulates
    it. Finally, the script reports the simulated execution time.

    This task expects four hydra parameters to be available.

    **Hydra Parameters**:
        * **kpn:** the input kpn graph. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.kpn.KpnGraph`
          object.
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        * **mapping:** the input mapping. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.mapping.Mapping`
          object.
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~pykpn.common.trace.TraceGenerator` object.
    """

    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    mapping = hydra.utils.instantiate(cfg['mapping'], kpn, platform)
    trace = hydra.utils.instantiate(cfg['trace'])

    env = simpy.Environment()
    app = RuntimeKpnApplication(name=kpn.name,
                                kpn_graph=kpn,
                                mapping=mapping,
                                trace_generator=trace,
                                env=env,)
    system = RuntimeSystem(platform, [app], env)

    start = timeit.default_timer()
    system.simulate()
    stop = timeit.default_timer()

    exec_time = float(env.now) / 1000000000.0
    print('Total simulated time: ' + str(exec_time) + ' ms')
    print('Total simulation time: ' + str(stop - start) + ' s')

    system.check_errors()
