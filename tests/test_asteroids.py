"""
Testing of asteroid package.
"""

import unittest
from pygame import Surface

from data import prepare
from data.components import asteroids

FAKE_GTX = {
        'asteroid': Surface((1, 1))  # fake asteroid image
}
FRAGMENTS = 3


class TestAsteroids(unittest.TestCase):
    """
    Tests of AsteroidsGroup class.
    """
    @classmethod
    def setUpClass(self):
        """
        Set fake global variables that are necessary.
        """
        asteroids.prepare.GTX = FAKE_GTX
        asteroids.FRAGMENTS = (FRAGMENTS, FRAGMENTS)

    def setUp(self):
        self.group = asteroids.AsteroidsGroup()

    def test_level_up_include_initial_setting(self):
        """
        Increase the number of asteroids each level
        """
        for i in range(5):
            self.assertEqual(i, self.group.round_level)
            self.assertEqual(i, self.group.asteroids_number)
            self.group.empty()
            self.group.next_level()

    def test_asteroid_fragmentation(self):
        """
        If asteroid is big enought, it fragments into higher-level asteroids

        For this test, minimum and maximum fragments is set to FRAGMENTS
        """
        for i in range(prepare.ASTEROIDS['level']):
            self.group.next_level()
            for asteroid_lvl in range(1, prepare.ASTEROIDS['level'] + 1):
                for index, asteroid in enumerate(self.group.sprites()):
                    self.assertEqual(asteroid_lvl, asteroid.level)
                    asteroids_before_kill = len(self.group) - 1
                    asteroid.kill()
                    fragments = len(self.group) - asteroids_before_kill
                    if asteroid_lvl != prepare.ASTEROIDS['level']:
                        self.assertEqual(3, fragments)
                    else:
                        self.assertEqual(0, fragments)
            self.assertEqual(0, len(self.group))
