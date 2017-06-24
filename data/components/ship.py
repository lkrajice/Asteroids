"""
This module contain Ship controlled by user and
other objects, that have close relation to ship.
"""

import math
import random
import pygame as pg

from . import components, laser
from .. import prepare, tools


SHIP_ENERGY_LOSS = 20
SHIP_BLINK_SPEED = 400  # both times when ship is fully visible and transparent
BLINK_COUNT = 10
SHIP_IMMORTAL_TIME = SHIP_BLINK_SPEED * BLINK_COUNT


class ShipPoint:
    """
    Class that exists just to hold informations about one point around ship.
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
    The class keps track about ships velocity, position, rotation etc...
    Separate math from GUI.
    """
    def __init__(self):
        components._MovingSprite.__init__(self, 'ship', prepare.SHIP['xy'])
        self.ship_size = self.original.get_size()
        self.rotate_speed = prepare.SHIP['rotate_speed'] / prepare.FPS
        self.acceleration = prepare.SHIP['acceleration']
        self.slow_factor = prepare.SHIP['slow_factor']
        self.max_speed = prepare.SHIP['max_speed']

    def rotate(self, side):
        """
        Update ships rotation.
        """
        angle = self.rotate_speed * side
        self.rotate_angle(angle)

    def accelerate(self):
        """
        Change ships speed.
        Method have to be called after changing rotation.
        """
        radians = math.radians(self.rotation)
        dx = self.dx + self.acceleration * math.cos(radians)
        dy = self.dy + self.acceleration * math.sin(radians)
        speed = math.hypot(dx, dy)
        if speed <= self.max_speed:
            self.dx = dx
            self.dy = dy
            self.speed = speed

    def slow_down(self):
        """
        Slow down ship by slow_factor and update ships speed.
        """
        radians = math.radians(self.rotation)
        self.dx *= self.slow_factor
        self.dy *= self.slow_factor
        self.speed = math.hypot(self.dx, self.dy)
        if self.speed < 0.15:
            self.dx = 0
            self.dy = 0
        # TODO calculate dx and dy with speed = 15

    def get_jet(self):
        """
        Return informations about poins near ship's jet.
        """
        direction = self._check_angle(self.rotation - 180)
        return self.get_ship_point(direction)

    def get_gun(self):
        """
        Return informations about poins near ship's head.
        """
        return self.get_ship_point(self.rotation)

    def get_ship_point(self, direction):
        """
        Calculate and returns some informations about the point near ship.
        Given direction specify the angle, where the point is located.
        """
        radians = math.radians(direction)
        x_center, y_center = self.get_position()
        width = self.ship_size[0]
        x_position = x_center + (self.ship_size[0] / 2) * math.cos(radians) * 2
        y_position = y_center - (self.ship_size[1] / 2) * math.sin(radians) * 2
        return ShipPoint(x_position, y_position, direction, self.dx, self.dy)


class Ship(_ShipTraction):
    """
    User's ship.
    """

    LEFT = 1
    RIGHT = -1

    def __init__(self):
        _ShipTraction.__init__(self)
        self.begin = -1
        self.now = 0
        self.immortal = True
        self.transparent = False
        self.blink_timer = tools.Timer(SHIP_BLINK_SPEED / 2,
                                       self.blink,
                                       BLINK_COUNT)

        self.colide_rotation = False
        self.energy_loss = SHIP_ENERGY_LOSS

        self.action_state = 'alive'
        self.smoke_generator = SmokeGenerator()
        self.ship_lasers = laser.Lasers()

        self.rotate_angle(90)

    def update(self, keys, now):
        """
        Slow down, then speed up, if user press a key.
        """
        self.now = now
        if self.begin == -1:
            self.begin = now

        self.slow_down()
        self.key_event()
        self.ship_lasers.update()
        self.rect = self.image.get_rect(center=self.get_position())

        self.blink_timer.check_tick(now)
        _ShipTraction.update(self)
        self.smoke_generator.update()

    def draw(self, surface):
        self.smoke_generator.draw(surface)
        self.ship_lasers.draw(surface)

        self.image.set_alpha(20)
        surface.blit(self.image, self.rect)

    def key_event(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.rotate(self.LEFT)
        elif keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.rotate(self.RIGHT)
        if keys[pg.K_UP]:
            self.accelerate()
            self.smoke_generator.create_particle(20, self.get_jet())

    def space_pressed(self):
        self.ship_lasers.fire(self.get_gun())

    def blink(self, ticks):
        if ticks == BLINK_COUNT:
            self.immortal = False
        if self.transparent:
            self.original.set_alpha(255)
        else:
            self.original.set_alpha
        self.transparent = not self.transparent


class SmokeParticle(components._FrameBasedSprite):
    """
    Smoke particle.
    """
    def __init__(self, *groups, jet=None):
        """
        Create random particle.
        """
        components._FrameBasedSprite.__init__(
                self,
                prepare.SMOKE['frames'],
                pg.Surface(prepare.SMOKE['size']),
                (0, 0))
        self.color = prepare.SMOKE['color'].copy()
        self.steps = prepare.SMOKE['rgb_change_per_frame']
        self.colide = False

        self.rotation = random.randint(0, 89)
        # Randomly select position with max deflection = 20
        center = list((x + random.randint(-20, 20)
                       for x in jet.get_position()))
        # Randomly set direction
        self.x = center[0]
        self.y = center[1]
        direction = math.radians(jet.direction + random.randint(-20, 20))
        self.dx = prepare.SMOKE['speed'] * math.cos(direction)
        self.dx += jet.dx
        self.dy = prepare.SMOKE['speed'] * math.sin(direction)
        self.dy += jet.dy

    def get_alpha_by_frame(self, frame, max_frames):
        return 256 - math.exp((frame * math.log(256)) / max_frames)

    def make_changes(self, frames):
        for index, step in enumerate(prepare.SMOKE['rgb_change_per_frame']):
            self.color[index] -= step
        self.alpha = self.get_alpha_by_frame(self.count, self.max_frames)


class SmokeGenerator(pg.sprite.RenderPlain):
    """
    Generator of smoke particles.
    """
    def __init__(self):
        pg.sprite.RenderPlain.__init__(self, [])

    def create_particle(self, number, jet):
        """
        Create number of particles.
        """
        for i in range(number):
            self.add(SmokeParticle(jet=jet))
