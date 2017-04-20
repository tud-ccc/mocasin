from unittest import TestCase

from pykpn.platforms import Tomahawk2Platform
from pykpn.platforms import GenericNocPlatform


class TestPlatforms(TestCase):
    def test_tomahawk2(self):
        Tomahawk2Platform()
        # There isn't really anything that we could assert here. If there
        # are no exceptions we are good.

    def test_generic(self):
        GenericNocPlatform('torus', 2, 4)
        GenericNocPlatform('mesh', 3, 8)
        GenericNocPlatform('torus', 3, 3)
        GenericNocPlatform('mesh', 8, 8)
