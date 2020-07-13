# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import hydra
import simpy

from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem


class BaseSimulation:
    """A generic simulation

    """

    def __init__(self, platform):
        self.env = simpy.Environment()
        self.platform = platform
        self.system = RuntimeSystem(platform, self.env)
        self.exec_time = None

    def run(self):
        raise NotImplementedError()

    def write_simulation_trace(self, path):
        self.system.trace_writer.write_trace(path)


class KpnSimulation(BaseSimulation):

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

    def _run_app(self):
        yield self.app.run()

    def run(self):
        # start all schedulers
        self.system.start_schedulers()
        # start the application
        self.env.process(self._run_app())
        # start the actual simulation
        self.env.run()
        # check if all kpn processes finished execution
        self.system.check_errors()
        # save the execution time
        self.exec_time = self.env.now

    @staticmethod
    def from_hydra(cfg):
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
