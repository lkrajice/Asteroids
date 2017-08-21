"""
Module implying lasers

Args:
    LASER_COLOR (:obj:`list` of :obj:`int`): color of the lasers in RGB

"""
import pygame as pg

from . import components
from .. import prepare

LASER_COLOR = (255, 255, 255)


class Lasers(pg.sprite.RenderPlain):
    """
    Laser gun

    Args:
        max (int): maximum lasers that can exists simultaneously

    """
    def __init__(self):
        super().__init__(list())
        self.max = 4

    def fire(self, gun):
        """
        Fire laser

        Args:
            gun (data.components.ship.ShipPoint): hold data about the point
                from witch lasers are fired, like dx, dy, rotation etc...

        """
        if len(self) < self.max:
            self.add(Laser(gun))


class Laser(components._FrameBasedSprite):
    """
    Laser shot

    `_FrameBasedSprite` automaticly kills sprite after final frame.

    Args:
        gun (data.components.ship.ShipPoint): hold data about the point from
            witch lasers are fired, like dx, dy, rotation etc...
        color (:obj:`list` of :obj:`int`): color of the lasers in RGB

    """
    def __init__(self, gun, color=LASER_COLOR):
        super().__init__(prepare.LASER['frames'],
                         prepare.LASER['img'],
                         gun.get_position())
        self.dx = gun.dx
        self.dy = gun.dy
        self.accelerate(gun.direction, prepare.LASER['speed'])
        self.update_color(color)

    def make_changes(self, frames):
        pass
