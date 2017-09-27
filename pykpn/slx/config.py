import configparser
import logging
import os

from pint import UnitRegistry
from pykpn.platforms import createPlatformByName

from .kpn import SlxKpnGraph
from .mapping import SlxMapping
from .trace import SlxTraceReader
from .platform import SlxPlatform


log = logging.getLogger(__name__)


class SlxConfig:

    def __init__(self, config):
        # read the ini file
        conf = configparser.ConfigParser()
        conf.read(config)

        # init function does all the parsing
        if 'platform_desc' in conf['simulation']:
            self.platform = SlxPlatform(conf['simulation']['platform_desc'])
        else:
            self.platform = createPlatformByName(conf['simulation']['platform'])

        self.app_names = conf['simulation']['applications'].split(",")

        if 'vcd' not in conf['simulation'] or conf['simulation']['vcd'] == '':
            self.vcd_file_name = None
        else:
            self.vcd_file_name = conf['simulation']['vcd']

        self.graphs = {}
        self.mappings = {}
        self.trace_readers = {}
        self.start_times = {}
        for an in self.app_names:
            if an not in conf:
                raise ValueError("application name does not match to the "
                                 "section key")
            graph = SlxKpnGraph(an + '_graph', conf[an]['graph'])
            mapping = SlxMapping(graph,
                                 self.platform,
                                 conf[an]['mapping'])

            trace_dir = os.path.join(conf[an]['trace'])
            assert os.path.isdir(trace_dir)
            reader = SlxTraceReader(trace_dir)

            self.graphs[an] = graph
            self.mappings[an] = mapping
            self.trace_readers[an] = reader
            self.vcd_file_name = conf['simulation']['vcd']
            ureg = UnitRegistry()
            time = conf[an]['start_time']
            self.start_times[an] = ureg(time).to(ureg.ps).magnitude
