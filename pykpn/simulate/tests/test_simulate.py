#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import simpy

from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform
from pykpn.simulate import System
from pykpn.simulate import Application
from pykpn.slx import SlxKpnGraph
from pykpn.slx import SlxMapping
from pykpn.slx import SlxTraceReader


class TestSimulate(TestCase):
    def test_slx(self):

        env = simpy.Environment()
        platform = Tomahawk2Platform(env)
        graph = SlxKpnGraph('graph', 'apps/pipeline/pipeline.cpn.xml')
        mapping = SlxMapping('apps/pipeline/default.mapping.consumer_bc')
        app = Application('app', graph, mapping, 'apps/pipeline/traces', SlxTraceReader)
        system = System(env, platform, [app], None)
        system.simulate()
