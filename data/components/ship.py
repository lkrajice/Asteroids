"""
Module implement ship and other close related objects

Args:
    SHIP_IMMORTAL_FRAMES (int): set interval of immortality right after
        spawning the ship

"""

import math
import random
import pygame as pg

from . import components, laser
from .. import prepare, tools

SHIP_IMMORTAL_FRAMES = 120


class ShipPoint:
    """
    Class that exists just to hold informations about one point around ship
    """
    def __init__(self, x, y, direction, dx, dy):
        self.x = x
        self.y = y
        self.direction = direction
        self.dx = dx
        self.dy = dy

    def get_position(self):
        return (self.x, self.y)


class _ShipTraction(components._MovingSprite):
    """
    Class containing math description of ship's movement

    The class keps track about ships velocity, position, rotation etc...
    Separate math from GUI.

    Attributes:
        LEFT (int): constant used when user rotates an `image` to the left
        RIGHT (int): constant used when user rotates an `image` to the left
        ship_size (:obj:`str` or :obj:`pygame.Surface`): sizes of the ship
        rotation_speed (float): determine rotation of the ship each frame when
        acceleration (float): acceleration of the ship per frame
        slow_factor (float): determine how large part of velocity will the
            ship lost each frame
        max_speed (float): maximum speed limit

    """

    LEFT = 1
    RIGHT = -1

    def __init__(self):
        super().__init__('ship', prepare.SHIP['xy'])
        self.ship_size = self.original.get_size()
        self.rotate_speed = prepare.SHIP['rotate_speed'] / prepare.FPS
        self.acceleration = prepare.SHIP['acceleration']
        self.slow_factor = prepare.SHIP['slow_factor']
        self.max_speed = prepare.SHIP['max_speed']

    def rotate(self, side):
        """
        Rotate the ship by `rotate_speed`

        Args:
            side (int): set on witch side the ship should rotate. `LEFT` and
                `RIGHT` values should be used for this argument

        """
        angle = self.rotate_speed * side
        self.rotate_angle(angle)

    def accelerate(self):
        """
        Change ships speed and check speed limit
        """
        radians = math.radians(self.rotation)
        self.dx += self.acceleration * math.cos(radians)
        self.dy += self.acceleration * math.sin(radians)
        speed = math.hypot(self.dx, self.dy)
        if speed > self.max_speed:
            speed_vector_angle = self._calculate_speed_vector_angle()
            dx = self.max_speed * math.cos(speed_vector_angle)
            dy = self.max_speed * math.sin(speed_vector_angle)
            self.dx = math.copysign(dx, self.dx)
            self.dy = math.copysign(dy, self.dy)

    def _calculate_speed_vector_angle(self):
        """
        Calculate actual velocity angle

        Returns:
            float: velocity angle in radians

        """
        try:
            return math.atan(self.dy / self.dx)
        except ZeroDivisionError:
            if self.dy > 0:
                return math.radians(90)
            else:
                return math.radians(270)

    def slow_down(self):
        """
        Slow down the ship by `slow_factor`

        If ship's total speed is lower then 0.05, set `dx` and `dy` to 0
        """
        self.dx *= 1 - self.slow_factor
        self.dy *= 1 - self.slow_factor
        self.speed = math.hypot(self.dx, self.dy)
        if self.speed < 0.05:
            self.dx = 0
            self.dy = 0

    def get_jet(self):
        """
        Return informations about poins near ship's jet
        """
        direction = self._check_angle(self.rotation - 180)
        return self.get_ship_point(direction)

    def get_gun(self):
        """
        Return informations about poins near ship's head
        """
        return self.get_ship_point(self.rotation)

    def get_ship_point(self, direction):
        """
        Calculate and returns some informations about the point near ship

        Args:
            direction (float): angle where the point can be found
        """
        radians = math.radians(direction)
        x_center, y_center = self.get_position()
        x_position = x_center + (self.ship_size[0] / 2) * math.cos(radians) * 2
        y_position = y_center - (self.ship_size[1] / 2) * math.sin(radians) * 2
        return ShipPoint(x_position, y_position, direction, self.dx, self.dy)


class Ship(_ShipTraction):
    """
    Extension of `_ShipTraction` by image management

    Rotate the ship by 90 degrees immediately.

    Attributes:
        immortal (bool): if True, ship can not collide with asteroids and other
            harmful objects
        smoke_generator (SmokeGenerator): generator of smoke particles
        ship_lasers (laser.Lasers): gun firing the laser
        immortal_timer (tools.Timer): timer that disable the immortality after
            `SHIP_IMMORTAL_FRAMES` frames

    """

    def __init__(self):
        super().__init__()
        self.immortal = True

        self.smoke_generator = SmokeGenerator()
        self.ship_lasers = laser.Lasers()
        self.immortal_timer = tools.Timer(
                SHIP_IMMORTAL_FRAMES / 60 * 1000,
                self.disable_immortality,
                ticks=1)

        self.rotate_angle(90)

    def update(self, now):
        """
        Slow down, then speed up, if user press a key
        """
        self.immortal_timer.check_tick(now)
        self.slow_down()
        self.key_event()
        self.ship_lasers.update()
        self.rect = self.image.get_rect(center=self.get_position())

        _ShipTraction.update(self)
        self.smoke_generator.update()

    def draw(self, surface):
        self.smoke_generator.draw(surface)
        self.ship_lasers.draw(surface)

        surface.blit(self.image, self.rect)

    def key_event(self):
        keys = pg.key.get_pressed()
        if ((keys[pg.K_LEFT] and not keys[pg.K_RIGHT]) or
                (keys[pg.K_a] and not keys[pg.K_d])):
            self.rotate(self.LEFT)
        elif ((keys[pg.K_RIGHT] and not keys[pg.K_LEFT]) or
                (keys[pg.K_d] and not keys[pg.K_a])):
            self.rotate(self.RIGHT)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.accelerate()
            self.smoke_generator.create_particle(20, self.get_jet())

    def space_pressed(self):
        """
        Notify gun about request to shoot laser
        """
        self.ship_lasers.fire(self.get_gun())

    def disable_immortality(self, *args):
        """
        Set `immortal` to False
        """
        self.immortal = False


class SmokeParticle(components._FrameBasedSprite):
    """
    Smoke particle

    Smoke particle generate own position. It jet as initial point and then it
    change its position with max deflection of 20.

    Every frame, color is changed in `make_changes` method.

    Args:
        jet (ShipPoint): holder of informations about jet

    Attributes:
        steps (:obj:`str` or :obj:`int`): change in color each frame

    """
    def __init__(self, jet):
        """
        Create random particle
        """
        pos = list((x + random.randint(-20, 20) for x in jet.get_position()))
        super().__init__(prepare.SMOKE['frames'],
                         pg.Surface(prepare.SMOKE['size']),
                         pos)

        self.colide = False
        self.steps = prepare.SMOKE['rgb_change_per_frame']

        direction = math.radians(jet.direction + random.randint(-20, 20))
        self.dx = prepare.SMOKE['speed'] * math.cos(direction)
        self.dx += jet.dx
        self.dy = prepare.SMOKE['speed'] * math.sin(direction)
        self.dy += jet.dy

        self.rotate_angle(random.randint(0, 89))
        self.update_color(prepare.SMOKE['color'].copy())

    @property
    def alpha_by_frame(self):
        """
        float: return how much transparent particle is each frame.
        """
        return 256 - math.exp((self.count * math.log(256)) / self.max_frames)

    def make_changes(self, frames):
        """
        Change color of the particle and alpha channel
        """
        color = self.color
        for index, step in enumerate(prepare.SMOKE['rgb_change_per_frame']):
            color[index] -= step
        self.update_color(color)
        self.alpha = self.alpha_by_frame


class SmokeGenerator(pg.sprite.RenderPlain):
    """
    Generator of smoke particles
    """
    def __init__(self):
        super().__init__([])

    def create_particle(self, number, jet):
        """
        Create particles

        Args:
            number (int): how much particles should be created
            jet (ShipPoint): holder of informations about jet

        """
        for i in range(number):
            self.add(SmokeParticle(jet))
