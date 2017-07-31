"""
Testing of components package.
"""

import unittest
from unittest.mock import patch
from pygame import Surface

from data import prepare
from data.components import components

FRAMES = 50

# changes in acceleration each update
ACCELERATION_STEPS = [
        {'angle': -48, 'acceleration': 26},
        {'angle': 318, 'acceleration': 7},
        {'angle': 132, 'acceleration': 10},
        {'angle': 138, 'acceleration': 7},
        {'angle': -228, 'acceleration': 16},
]

SPEED_STEPS = [
        {'dx': 3, 'dy': 5},
        {'dx': -8, 'dy': 12},
        {'dx': 17, 'dy': 3},
        {'dx': 2, 'dy': 0},
        {'dx': -4, 'dy': -22},
        {'dx': -10, 'dy': 2},
]


class FrameBasedSprite(components._FrameBasedSprite):
    """
    Child of uninstantiable _FrameBasedSprite.
    """
    def make_changes(self, frame):
        pass


class TestFrameBasedSprite(unittest.TestCase):
    """
    Tests of _FrameBasedSprite class.
    """
    def setUp(self):
        self.sprite = FrameBasedSprite(
                FRAMES,
                Surface((100, 100)),
                prepare.SCREEN_RECT.center)

    @patch('tests.test_components.FrameBasedSprite.kill')
    @patch('tests.test_components.FrameBasedSprite.make_changes')
    def test_life_cycle(self, mock_make_changes, mock_kill):
        """
        _FrameBasedSprite change every update, then it `kill()`s itself
        """
        for i in range(1, FRAMES):
            self.sprite.update()
            self.assertEqual(i, len(mock_make_changes.call_args_list))
            mock_make_changes.assert_called_with(i)
        mock_make_changes.reset_mock()
        mock_kill.assert_not_called()

        self.sprite.update()
        mock_kill.assert_called_once_with()
        mock_make_changes.assert_not_called()


class TestMovingSprite(unittest.TestCase):
    """
    Tests of _MovingSprite class.
    """
    def setUp(self):
        self.sprite = components._MovingSprite(
                Surface((1, 1)),
                prepare.SCREEN_RECT.center)

    def test_bouncing_off_the_edges(self):
        """
        _MovingSprite bounce off the screen edges instead of go through
        """
        components.ENERGY_LOSS = 0
        self.sprite.dx, self.sprite.dy = 500, 500
        for i in range(10):
            self.sprite.update()
            for positions in zip(self.sprite.get_position(),
                                 prepare.SCREEN_SIZE):
                self.assertGreaterEqual(positions[0], 0)
                self.assertLessEqual(positions[0], positions[1])

    def test_acceleration(self):
        """
        _MovingSprite accelerate correctly
        """
        for step in ACCELERATION_STEPS:
            self.sprite.accelerate(step['angle'], step['acceleration'])
        for direction_speed in (self.sprite.dx, self.sprite.dy):
            self.assertAlmostEqual(0, direction_speed, 14)

    def test_movement(self):
        """
        _MovingSprite moves correctly due to dx and dy
        """
        initial_position = self.sprite.get_position()
        for step in SPEED_STEPS:
            self.sprite.dx, self.sprite.dy = step['dx'], step['dy']
            self.sprite.update()
        self.assertEqual(initial_position, self.sprite.get_position())
