import configparser
import logging
import os

from pint import UnitRegistry
from pykpn.platforms import createPlatformByName

from .kpn import SlxKpnGraph
from .mapping import SlxMapping
from .trace import SlxTraceReader


log = logging.getLogger(__name__)


class SlxConfig:

    def __init__(self, config):
        # read the ini file
        conf = configparser.ConfigParser()
        conf.read(config)

        # init function does all the parsing
        self.platform = createPlatformByName(conf['simulation']['platform'])
        self.app_names = conf['simulation']['applications'].split(",")

        if 'vcd' not in conf['simulation'] or conf['simulation']['vcd'] == '':
            self.vcd_file_name = None
        else:
            self.vcd_file_name = conf['simulation']['vcd']

        self.graphs = {}
        self.mappings = {}
        self.trace_readers = {}
        self.mapping_to_dot = {}
        self.start_times = {}
        for an in self.app_names:
            if an not in conf:
                raise ValueError("application name does not match to the "
                                 "section key")
            graph = SlxKpnGraph(an + '_graph', conf[an]['graph'])
            mapping = SlxMapping(graph,
                                 self.platform,
                                 conf[an]['mapping'])

            readers = {}
            for pm in mapping.processMappings:
                name = pm.kpnProcess.name
                trace_dir = os.path.join(conf[an]['trace'])
                assert os.path.isdir(trace_dir)
                readers[name] = SlxTraceReader(name, an, trace_dir)

            self.graphs[an] = graph
            self.mappings[an] = mapping
            self.trace_readers[an] = readers
            if 'mappingout' not in conf[an] or conf[an]['mappingout'] == '':
                self.mapping_to_dot[an] = None
            else:
                self.mapping_to_dot[an] = conf[an]['mappingout']
            self.vcd_file_name = conf['simulation']['vcd']
            ureg = UnitRegistry()
            time = conf[an]['start_time']
            self.start_times[an] = ureg(time).to(ureg.ps).magnitude
