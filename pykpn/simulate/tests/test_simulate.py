#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform
from pykpn.simulate import System
from pykpn.simulate import Application
from pykpn.slx import SlxKpnGraph
from pykpn.slx import SlxMapping
from pykpn.slx import SlxTraceReader


class TestSimulate(TestCase):
    def test_slx(self):

        platform = Tomahawk2Platform()
        graph = SlxKpnGraph('graph', 'apps/pipeline/pipeline.cpn.xml')
        mapping = SlxMapping(graph,
                             platform,
                             'apps/pipeline/default.mapping.consumer_bc')

        readers = {}
        for pm in mapping.processMappings:
            name = pm.kpnProcess.name

            processors = pm.scheduler.processors
            type = processors[0].type
            path = 'apps/pipeline/traces/' + name + '.' + type + '.cpntrace'
            readers[name] = SlxTraceReader(path, 'app')

        app = Application('app', graph, mapping, readers, 0)
        system = System(None, platform, [app])
        system.simulate()
