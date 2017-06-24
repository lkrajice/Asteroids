"""
Asteroids.
"""

import math
import random
import pygame as pg

from . import components
from .. import prepare


FRAGMENTS = (2, 4)
SPEED = (2, 3)
DEGREE_DEADZONE = 20


class AsteroidsGroup(pg.sprite.RenderPlain):
    """
    Own all asteroids and take care of its creations and fragmentations.
    """
    def __init__(self):
        pg.sprite.RenderPlain.__init__(self, [])
        self.round_level = 0
        self.asteroids_number = 0

    def create_asteroids(self, number, level, pos=prepare.SCREEN_RECT.center):
        for i in range(number):
            self.add(Asteroid(level, pos, self.fragment_asteroid))

    def next_level(self):
        self.round_level += 1
        self.asteroids_number += 1
        self.create_asteroids(self.asteroids_number, 1)

    def fragment_asteroid(self, asteroid):
        fragments = random.randint(*FRAGMENTS)
        level = asteroid.level + 1
        position = asteroid.get_position()
        self.create_asteroids(fragments, level, position)


class Asteroid(components._MovingSprite):
    """
    Asteroid class. Exists in various levels, max level is
    prepare.ASTEROIDS['level']]. Higher level makes speed higher and
    image sizes smaller.
    """
    def __init__(self, level, position, kill_callback):
        components._MovingSprite.__init__(self, 'asteroid', position)
        old_sizes = self.original.get_size()
        self.level = level

        scale = math.pow(2, self.level - 1)
        self.sizes = list(map(int, (size / scale for size in old_sizes)))
        original = pg.transform.scale(self.original, self.sizes)
        self.set_original(original)

        self.kill_callback = kill_callback

        speed = random.randint(*SPEED) + self.level
        direction = random.randint(0 + DEGREE_DEADZONE, 90 - DEGREE_DEADZONE)
        direction += 90 * random.randint(0, 3)
        self.dx = speed * math.cos(direction)
        self.dy = speed * math.sin(direction)
        if self.level == 1:
            self.set_initial_position()

    def set_initial_position(self):
        """
        Set asteroids position out of the screen
        """
        self.x += math.copysign(self.x + self.sizes[0], self.dx)
        self.y -= math.copysign(self.y + self.sizes[1], self.dy)

    def kill(self):
        """
        Fragment itself, then disappear.
        """
        if self.level < prepare.ASTEROIDS['level']:
            self.kill_callback(self)
        components._MovingSprite.kill(self)
