# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import configparser
import os

import pint

import pykpn.platforms
from pykpn.util import logging


log = logging.getLogger(__name__)


class SlxApplicationConfig:
    """INI parser for application sections

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

    def __init__(self, config_file):
        """Initialize config object by parsing an INI file.

        :param str config_file: configuration file to be parsed
        """

        # read the ini file
        conf = configparser.ConfigParser()
        conf.read(config_file)

        # parse the ini version
        version = conf['simulation']['slx_version']
        self.slx_version = version

        # parse the platform
        if 'platform' in conf['simulation']:
            platform = conf['simulation']['platform']
            self.platform_class = getattr(pykpn.platforms, platform)
            self.platform_xml = None
        else:
            platform_xml = conf['simulation']['platform_xml']
            if not os.path.isfile(platform_xml):
                raise ValueError('The platform description does not exist: %s' %
                                 platform_xml)
            self.platform_xml = platform_xml
            self.platform_class = None

        # parse all applications
        app_names = conf['simulation']['applications'].split(",")
        self.applications = []
        for an in app_names:
            self.applications.append(SlxApplicationConfig(an, conf))
