# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import configparser
import os

import pint

import pykpn.platforms
from pykpn.util import logging


log = logging.getLogger(__name__)


class SlxApplicationConfig:
    """INI parser for application sections.


    :ivar str name: application name
    :ivar str mapping_xml: path to the mapping descriptor
    :ivar str cpn_xml: path to the cpn graph descriptor
    :ivar str trace_dir: path to the trace directory
    :ivar int start_at_tick: tick at which the application starts
    """

    def __init__(self, name, conf):
        """Initialize application config object by parsing a section of an INI
        file.

        :param str name: name of the application section to be parsed
        :param ConfigParser conf: a config parser object
        """
        self.name = name

        # parse the mapping
        mapping_xml = conf[name]['mapping_xml']
        if not os.path.isfile(mapping_xml):
            raise ValueError('The mapping description does not exist: %s' %
                             mapping_xml)
        self.mapping_xml = mapping_xml

        # parse the cpn graph
        cpn_xml = conf[name]['cpn_xml']
        if not os.path.isfile(cpn_xml):
            raise ValueError('The cpn graph description does not exist: %s' %
                             cpn_xml)
        self.cpn_xml = cpn_xml

        # parse the trace dir
        trace_dir = conf[name]['trace_dir']
        if not os.path.isdir(trace_dir):
            raise ValueError('The trace directory does not exist: %s' %
                             trace_dir)
        self.trace_dir = trace_dir

        # parse the start time
        ureg = pint.UnitRegistry()
        time = conf[name]['start_time']
        self.start_at_tick = ureg(time).to(ureg.ps).magnitude


class SlxSimulationConfig:
    """INI parser for simulation configurations

    A template for a valid ini file can be found in conf/slx_config.ini.

    :ivar str platform_xml: path to the platform descriptor
    :ivar str slx_version: slx version string
    :ivar applications: list of application configurations
    :type applications: list[SlxApplicationConfig]
    """

    def __init__(self, config_file=None, config_dict=None):
        """Initialize config object by parsing an INI file.

        :param str config_file: configuration file to be parsed
        :param str config_dict: configuration dictionary: overides values from configuration file
        """

        if config_file == None and config_dict == None:
            log.error("No configuration supplied.")

        # read the ini file
        if not config_file is None:
            conf = configparser.ConfigParser()
            conf.read(config_file)

            # parse the ini version
            version = conf['simulation']['slx_version']
            self.slx_version = version
        if not config_dict is None:
            if 'slx_version' in config_dict:
                self.slx_version = config_dict['slx_version']
            else:
                if config_file is None:
                    log.error("Incomplete configuration. Missing slx_version")



        # parse the platform
        platform = None
        if not config_file is None:
            if 'platform' in conf['simulation']:
                platform = conf['simulation']['platform']
        if not config_dict is None:
            if 'platform' in config_dict:
                platform = config_dict['platform']

        if not platform is None:
            self.platform_class = getattr(pykpn.platforms, platform)
            self.platform_xml = None

        else:
            if not config_file is None:
                platform_xml = conf['simulation']['platform_xml']
            if not config_dict is None:
                if 'platform_xml' in config_dict:
                    platform_xml = config_dict['platform_xml']

            print(os.getcwd())
            if not os.path.isfile(platform_xml):
                raise ValueError('The platform description does not exist: %s' %
                                 platform_xml)
            self.platform_xml = platform_xml
            self.platform_class = None

        # parse all applications
        if not config_file is None:
            #legacy multi-app:
            app_names = conf['simulation']['applications'].split(",")
            self.applications = []
            for an in app_names:
                self.applications.append(SlxApplicationConfig(an, conf))
        if not config_dict is None and 'app_name' in config_dict:
            dummy_conf = {config_dict['app_name']: config_dict}
            #hydra: single-app per execution
            self.applications = [SlxApplicationConfig(config_dict['app_name'],dummy_conf)]
