import configparser
import os

import pint

import pykpn.platforms
from pykpn.common import logging


log = logging.getLogger(__name__)

class SingleConfig:
    # container for a single app-platform combination
    def __init__(self, app, platform):
        self.app_name = app
        self.platform_name = platform
        self.platform_xml = 'apps/' + app + '/' + platform + '/' + platform + '.platform'
        self.mapping_xml = 'apps/' + app + '/' + platform + '/default.mapping'
        self.cpn_xml = 'apps/' + app + '/' + app + '.cpn.xml'
        self.trace_dir = 'apps/' + app + '/' + platform + '/traces'
        self.out_dir = 'apps/' + app + '/' + platform + '/results'


def to_int(str):
    return int(str)

def to_str(str):
    return str

def to_float_list(str):
    res = []
    for f in str.split(','):
        res.append(float(f))
    return res

def to_bool(str):
    return str == "True"

def to_time(str):
    ureg = pint.UnitRegistry()
    return ureg(str).to(ureg.ps).magnitude


class GlobalConfig:
    # parser for the new settings.ini

    def __init__(self, config_file):

        conf = configparser.ConfigParser()
        conf.read(config_file)

        # create app-platform combinations
        self.system = {}

        self.keys = {'slx_version' : to_str,
                     'start_time' : to_time,
                     'max_samples' : to_int,
                     'adapt_samples' : to_int,
                     'hitting_propability' : to_float_list,
                     'deg_p_polynomial' : to_int,
                     'step_width' : to_float_list,
                     'deg_s_polynomial' : to_int,
                     'max_step' : to_int,
                     'show_polynomials' : to_bool,
                     'show_points' : to_bool,
                     'max_pe' : to_int,
                     'distr' : to_str,
                     'shape' : to_str,
                     'oracle' : to_str,
                     'random_seed' : to_int,
                     'threshold' : to_int,
                     'run_perturbation' : to_bool,
                     'num_perturbations' : to_int,
                     'representation' : to_str
                     }

        if not 'default' in conf:
            raise ValueError('Settings.ini must contain a \'default\' section')

        for pl in conf['default']['platforms'].split(','):
            for app in conf['default']['apps'].split(','):
                combined_name = app+'/'+pl
                if (combined_name in conf) and (not conf[combined_name].getboolean('blacklist', False)):
                    self.system[combined_name] = SingleConfig(app, pl)
                elif not (combined_name in conf):
                    self.system[combined_name] = SingleConfig(app, pl)

        for cname in self.system.keys():
            for k in self.keys.keys():
                if cname in conf and k in conf[cname]:
                    setattr(self.system[cname], k, self.keys[k](conf[cname].get(k)) )
                else:
                    setattr(self.system[cname], k, self.keys[k](conf['default'].get(k)))

