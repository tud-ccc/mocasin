# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import os

from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.mapping import SlxMapping
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.trace import SlxTraceReader


class SlxRuntimeSystem(RuntimeSystem):
    """SLX specialization of the RuntimeSystem class"""

    def __init__(self, config, env):
        """Initialize a slx runtime system object

        :param SlxSimulationConfig config: an slx simulation config object
        :param simpy.Environment env: the simpy environment
        """
        name = os.path.splitext(os.path.basename(config.platform_xml))[0]
        platform = SlxPlatform(name, config.platform_xml, config.slx_version)

        applications = []
        for app_config in config.applications:
            name = app_config.name
            kpn = SlxKpnGraph(name, app_config.cpn_xml, config.slx_version)
            mapping = SlxMapping(kpn, platform,
                                 app_config.mapping_xml,
                                 config.slx_version)
            trace_reader = SlxTraceReader.factory(app_config.trace_dir,
                                                  '%s.' % (app_config.name),
                                                  config.slx_version)
            app = RuntimeKpnApplication(name, kpn, mapping, trace_reader, env,
                                        app_config.start_at_tick)
            applications.append(app)

        super().__init__(platform, applications, env)
