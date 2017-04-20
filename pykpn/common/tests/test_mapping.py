#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform
from pykpn.slx import SlxMapping
from pykpn.slx import SlxKpnGraph


class TestMapping(TestCase):
    def test_mappingToDot(self):
        platform = Tomahawk2Platform()
        graph = SlxKpnGraph('graph', 'apps/pipeline/pipeline.cpn.xml')
        mapping = SlxMapping(graph,
                             platform,
                             'apps/pipeline/default.mapping.consumer_bc')
        mapping.toPyDot()
