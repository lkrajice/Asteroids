"""
Basic laser object.
"""
import math
import pygame as pg

from . import components
from .. import prepare


LASER_COLOR = (255, 255, 255)

class Lasers(pg.sprite.RenderPlain):
    """
    Laser gun, max 4 lasers simultaneously.
    """
    def __init__(self):
        pg.sprite.RenderPlain.__init__(self, [])
        self.max = 4

    def fire(self, gun):
        """
        4 lasers at maximum.
        """
        if len(self) < self.max:
            self.add(Laser(gun))


class Laser(components._FrameBasedSprite):
    def __init__(self, gun, color=LASER_COLOR):
        components._FrameBasedSprite.__init__(self,
                                              prepare.LASER['frames'],
                                              prepare.LASER['img'],
                                              gun.get_position())
        self.dx = gun.dx
        self.dy = gun.dy
        self.color = color
        self.rotation = gun.direction
        self.rect = self.image.get_rect(center=gun.get_position())

        self.accelerate(self.rotation, prepare.LASER['speed'])
