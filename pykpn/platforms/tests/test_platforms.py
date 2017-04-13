import simpy

from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform


class TestPlatforms(TestCase):
    def test_tomahawk2(self):
        env = simpy.Environment()
        th2 = Tomahawk2Platform(env)
        # There isn't really anything that we could assert here. If there
        # are no exceptions we are good.
