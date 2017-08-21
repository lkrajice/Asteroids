"""
Module implying asteroids

Args:
    FRAGMENTS (:obj:`tuple` of :obj:`int`): set minimum and maximum fragments
        when asteroid fragmentation occur
    SPEED (:obj:`tuple` of :obj:`int`): set minumum and maximum speed for
        asteroids level 1. Higher level asteroids just add bonus speed to this
        velocity.
    DEGREE_DEADZONE (int): specify span round 0°, 90°, 180° 270° angle that
        the asteroid can not have. If `DEGREE_DEADZONE` is 10, asteroid
        velocity angle cannot be (-10; 10), (80; 100), (170; 190), (260; 280)

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
    Group cantains all asteroids. Also provide some useful methods.

    Attributes:
        round_level (int): current game level
        asteroids_number (int): tells how much asteroids were created this
            round

    """
    def __init__(self):
        super().__init__(list())
        self.round_level = 0
        self.asteroids_number = 0

    def create_asteroids(self, number, level, pos=prepare.SCREEN_RECT.center):
        """
        Create asteroids

        Set `kill_callback` of the asteroid to the `fragment_asteroid`.

        Args:
            number (int): number of asteroids to create
            level (int): level of asteroids that will be created
            pos (:obj:`tuple`of :obj:`int`): position where asteroid appears

        """
        for i in range(number):
            self.add(Asteroid(level, pos, self.fragment_asteroid))

    def next_level(self):
        """
        Shift to next level, spawn new asteroids
        """
        self.round_level += 1
        self.asteroids_number += 1
        self.create_asteroids(self.asteroids_number, 1)

    def fragment_asteroid(self, asteroid):
        """
        Fragment given asteroids or erase them

        Args:
            asteroid (Asteroid): asteroid to be erased. If its level is low
                enought, new asteroids will be created. If not, asteroid just
                disappear

        """
        fragments = random.randint(*FRAGMENTS)
        level = asteroid.level + 1
        position = asteroid.get_position()
        self.create_asteroids(fragments, level, position)


class Asteroid(components._MovingSprite):
    """
    Asteroid object

    It exists in various levels, max level is `prepare.ASTEROIDS['level']]`.
    Higher level makes speed higher and image size smaller.

    Args:
        level (int): level to be set to this asteroid
        position (:obj:`tuple`of :obj:`int`): position where asteroid appears
        kill_callback (function): function that is called when asteroid's
            `kill` method was called and asteroids's level is not the highest
            one. The method should take care about fragmentation.

    Attributes:
        size (:obj:`tuple` of :obj:`int`): width and height of the asteroid
        dx (float): speed in x direction
        dy (float): speed in x direction

    """
    def __init__(self, level, position, kill_callback):
        super().__init__('asteroid', position)
        old_size = self.original.get_size()
        self.level = level

        scale = math.pow(2, self.level - 1)
        self.size = list(map(int, (size / scale for size in old_size)))
        original = pg.transform.scale(self.original, self.size)
        self.set_original(original)

        speed = random.randint(*SPEED) + self.level
        direction = random.randint(DEGREE_DEADZONE, 90 - DEGREE_DEADZONE)
        direction += 90 * random.randint(0, 3)
        self.dx = speed * math.cos(math.radians(direction))
        self.dy = speed * math.sin(math.radians(direction))

        if self.level == 1:
            self.set_initial_position()
        self.kill_callback = kill_callback

    def set_initial_position(self):
        """
        Set asteroids initial position out of the screen

        Asteroids with level one are directly created, they wasn't created
        during fragmentation proccess. To evade just ugly appears in one frame,
        this method set initial position out of the screen.
        """
        self.x -= math.copysign(self.x + self.size[0], self.dx)
        self.y += math.copysign(self.y + self.size[1], self.dy)

        if self.dx < self.dy:
            shift = random.randint(0, prepare.SCREEN_SIZE[0] / 2)
            self.x -= math.copysign(shift, self.x)
        else:
            shift = random.randint(0, prepare.SCREEN_SIZE[1] / 2)
            self.y -= math.copysign(shift, self.x)

        self.update_rect()

    def kill(self):
        """
        Fragment itself if have enought low level or just disappear
        """
        if self.level < prepare.ASTEROIDS['level']:
            self.kill_callback(self)
        components._MovingSprite.kill(self)
