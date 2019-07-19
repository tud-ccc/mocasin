import configparser
import os
import logging
import pint

import pykpn.platforms
from itertools import product

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

class Setting:
    # container for a setting
    # attributes get later
    def __init__(self, idx):
        self.idx = idx

def to_int(s):
    res = []
    for f in s.split(','):
        res.append(int(f))
    return res

def to_float(s):
    res = []
    for f in s.split(','):
        res.append(float(f))
    return res

def to_str(s):
    res = []
    for f in s.split(','):
        res.append(f)
    return res

def to_float_list(s):
    res = []
    for f in s.split(','):
        part_res = []
        for g in s.split(' '):
            part_res.append(float(g))
        res.append(part_res)
    return res

def to_bool(s):
    res = []
    for f in s.split(','):
        res.append(f == 'True')
    return res

def to_time(s):
    ureg = pint.UnitRegistry()
    res = []
    for f in s.split(','):
        res.append(ureg(f).to(ureg.ps).magnitude)
    return res

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
                     'starting_radius' : to_float,
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
                     'num_reference_mappings' : to_int,
                     'representation' : to_str,
                     'keep_metrics' : to_bool,
                     'adaptable_center_weights' : to_bool,
                     'visualize_mappings' : to_bool
                     }

        if not 'default' in conf:
            raise ValueError('Settings.ini must contain a \'default\' section')

        names = []
        for pl in conf['default']['platforms'].split(','):
            for app in conf['default']['apps'].split(','):
                combined_name = app+'/'+pl
                if (combined_name in conf) and (not conf[combined_name].getboolean('blacklist', False)):
                    names.append(combined_name)
                    self.system[combined_name] = {}
                    self.system[combined_name]['sconf'] = SingleConfig(app,pl)
                    self.system[combined_name]['settings'] = []

                #elif not (combined_name in conf):
                #    names.append(combined_name)
                #    self.system[combined_name] = {}
                #    self.system[combined_name]['sconf'] = SingleConfig(app,pl)
                #    self.system[combined_name]['settings'] = []

        log.info(f"Execution on combinations: {names}")
        for cname in names:
            setting = {}
            for k in self.keys.keys():

                if cname in conf and k in conf[cname]:
                    setting[k] = self.keys[k](conf[cname].get(k))
                else:
                    setting[k] = self.keys[k](conf['default'].get(k))

            # print("Setting:")
            # print(setting)
            # print("\n")

            c_prod_dict = []
            c_prod_dict = (dict(zip(setting, x)) for x in product(*setting.values()))
            #for values in product(setting.values()):
            #    c_prod_dict.append(dict(zip(setting.keys(), values)))

            # print("product:")
            # print(c_prod_dict)
            # print("\n")

            for i,d in enumerate(c_prod_dict):
                self.system[cname]['settings'].append(Setting(i))
                for attr in self.keys.keys():
                    setattr(self.system[cname]['settings'][i], attr, d[attr])
