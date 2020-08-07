# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import hydra
import simpy

from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem


class BaseSimulation:
    """A base class for handling a simulation

    Attributes:
        env (~simpy.core.Environment): the simpy environment
        platform (Platform): the platform that is simulated by this object
        system (RuntimeSystem): runtime representation of the simulated system
        exec_time (int): total simulated time in ps. This is initial to
            ``None`` and only set after a call to :func:`run`.

    Args:
        platform (Platform): the platform that is simulated by this object
    """

    def __init__(self, platform):
        self.env = simpy.Environment()
        self.platform = platform
        self.system = RuntimeSystem(platform, self.env)
        self.exec_time = None

    def run(self):
        """Run the simulation

        This needs to be overridden by a  subclass

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def write_simulation_trace(self, path):
        """Write a json trace of the simulated system to ``path``

        The generated trace can be opened with Chrome's or Chromiums builtin
        trace viewer at ``about://tracing/``.

        This should only be called after calling func:`run`.

        Args:
            path (str): path to the file that should be generated
        """
        self.system.trace_writer.write_trace(path)

    def enable_tracing(self):
        """Enable simulation trace generation"""
        self.system.trace_writer.enable()

    def disable_tracing(self):
        """Disable simulation trace generation"""
        self.system.trace_writer.disable()


class KpnSimulation(BaseSimulation):
    """Handles the simulation of a single KPN application

    Attributes:

    Args:
        platform (Platform): the platform that is simulated by this object
        kpn (KpnGraph): the KPN application to be executed on the given
            ``platform``
        mapping (Mapping): a mapping of the ``kpn`` to the ``platform``
        trace (TraceGenerator): a trace generator for the given ``kpn``
    """

    def __init__(self, platform, kpn, mapping, trace):
        super().__init__(platform)
        self.kpn = kpn
        self.mapping = mapping
        self.trace = trace
        self.app = RuntimeKpnApplication(name=kpn.name,
                                         kpn_graph=kpn,
                                         mapping=mapping,
                                         trace_generator=trace,
                                         system=self.system)

    def run(self):
        """Run the simulation.

        May only be called once. Updates the :attr:`exec_time` attribute.
        """
        if self.exec_time is not None:
            raise RuntimeError("A KpnSimulation may only be run once!")

        # start all schedulers
        self.system.start_schedulers()
        # start the application
        finished = self.env.process(self.app.run())
        # run the actual simulation until the application finishes
        self.env.run(finished)
        # check if all kpn processes finished execution
        self.system.check_errors()
        # save the execution time
        self.exec_time = self.env.now

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`KpnSimulation` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        platform = hydra.utils.instantiate(cfg['platform'])
        kpn = hydra.utils.instantiate(cfg['kpn'])
        mapper = hydra.utils.instantiate(cfg['mapper'], kpn, platform, cfg)
        mapping = mapper.generate_mapping()
        trace = hydra.utils.instantiate(cfg['trace'])
        simulation = KpnSimulation(platform, kpn, mapping, trace)
        return simulation


# workaround until we can call the static method above directly from hydra 1.0
class HydraKpnSimulation(KpnSimulation):
    def __new__(cls, cfg):
        return KpnSimulation.from_hydra(cfg)
