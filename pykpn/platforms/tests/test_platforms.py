import simpy

from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform
from pykpn.platforms import GenericNocPlatform


class TestPlatforms(TestCase):
    def test_tomahawk2(self):
        env = simpy.Environment()
        th2 = Tomahawk2Platform(env)
        # There isn't really anything that we could assert here. If there
        # are no exceptions we are good.

    def test_generic(self):
        env= simpy.Environment()
        th0=GenericNocPlatform(env, 'torus', 2, 4)
        th1=GenericNocPlatform(env, 'mesh', 3, 8)
        th2=GenericNocPlatform(env, 'torus', 3, 3)
        th3=GenericNocPlatform(env, 'mesh', 8, 8)
