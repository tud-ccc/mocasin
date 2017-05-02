import configparser
import re

from pint import UnitRegistry
from pykpn.platforms import createPlatformByName

class SlxConfig:
    def __init__(self, config):
        self.conf=configparser.ConfigParser()
        self.conf.read(config)
        self.applications=self.get_apps()

    def get_platform(self):
        return createPlatformByName(self.conf['simulation']['platform'])

    def get_apps(self):
        return self.conf['simulation']['applications'].split(",")

    def get_trace(self, app):
        return self.conf[app]['trace']

    def get_mapping(self, app):
        return self.conf[app]['mapping']

    def get_graph(self, app):
        return self.conf[app]['graph']

    def get_vcd(self):
        return self.conf['simulation']['vcd']

    def get_mappingout(self, app):
        if 'mappingout' not in self.conf[app]:
            return False
        else:
            return self.conf[app]['mappingout']

    def get_ini_time(self, app):
        ureg = UnitRegistry()
        return ureg(self.conf[app]['ini_time']).to(ureg.ps).magnitude
