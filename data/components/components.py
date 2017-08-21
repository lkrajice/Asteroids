"""
Module implements some
"""
import abc
import math
import pygame as pg

from .. import prepare

ENERGY_LOSS = 0
ENERGY_REMAINS = 1 - (ENERGY_LOSS / 100)


class _MovingSprite(pg.sprite.Sprite, metaclass=abc.ABCMeta):
    """
    Abstract advanced sprite. It's able to tracks position, speed and do
    various kinds of calculations. It takes care about movement, rotation and
    interacting with sides of the sreen.

    Args:
        img (:obj:`str` or :obj:`pygame.Surface`):
        position (:obj:`tuple`of :obj:`int`): ship's initial position

    Attributes:
        colite (bool): if True, object bounce off the `move_rect` instead of
            go through
        move_rect (pg.Rect): rectangle in witch Sprite moves. But if `colide`
            is set to True, this rectangle is ignored
        dx (float): speed in x direction
        dy (float): speed in y direction
        rotation (int): current rotation of the ship
        image_changed (bool): determine if image changed, if so, `image` is
            recreated, same with `rect`
        color_changed (bool): determine if color changed
        original (pg.Surface): original image of the ship. This image should
            not be ever changed to preserve original image quality. It is used
            every time, when `image` need recreation.
        rect (pg.Rect): rectangle of the `image`
        x (int): position in x direction
        y (int): position in y direction
        image (pygame.Surface): the ship's image that user actualy see.
            `original` image is used every time when creating new `image` to
            preserve image quality.
        color (:obj:`tuple`of :obj:`int`): color to `fill` `image` with in RGB
        alpha (int): alpha of the image <0; 255>

    """

    def __init__(self, img, position):
        super().__init__([])
        self.colide = True
        self.move_rect = prepare.SCREEN_RECT

        self.dx = 0.0
        self.dy = 0.0
        self.rotation = 0

        self.image_changed = True
        self.color_changed = True

        self.original = prepare.GTX[img] if isinstance(img, str) else img
        self.rect = self.original.get_rect(center=position)
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.image = None
        self.color = None
        self.alpha = 255

        self.update_image()

    def _check_position(self):
        """
        Check, if object does not overrun allowed rectangle

        If `rect` pass beyond `move_rect`, corresponding velocity is reverset
        and reduced an well as the rect is shifted to the position as if the
        rect bounced.

        Special situations are objects that are beyond `move_rect` but its
        velocity is dirrected to the `move_rect`. If so, object is ignore.
        For example asteroids can 'enter' the `move_rect` from outside without
        any velocity reduction or position shift.

        Set `colide` to False to bypass.
        """
        difference = {'x': 0, 'y': 0}
        if self.rect.right > self.move_rect.right and self.dx > 0:
            difference['x'] = self.move_rect.right - self.rect.right
        elif self.rect.left < self.move_rect.left and self.dx < 0:
            difference['x'] = self.move_rect.left - self.rect.left
        if self.rect.top < self.move_rect.top and self.dy > 0:
            difference['y'] = self.move_rect.top - self.rect.top
        elif self.rect.bottom > self.move_rect.bottom and self.dy < 0:
            difference['y'] = self.move_rect.bottom - self.rect.bottom
        if difference['x'] is not 0:
            self._bounce_in_x_direction(difference['x'])
        elif difference['y'] is not 0:
            self._bounce_in_y_direction(difference['y'])
        else:
            return
        self._check_position()

    def _bounce_in_x_direction(self, difference):
        self.dx *= -ENERGY_REMAINS
        shift = difference * (1 + ENERGY_REMAINS)
        self.move(shift, 0)

    def _bounce_in_y_direction(self, difference):
        self.dy *= -ENERGY_REMAINS
        shift = difference * (1 + ENERGY_REMAINS)
        self.move(0, shift)

    def move(self, x_shift, y_shift):
        """
        Moves the rect by given values

        Args:
            x_shift (float): determine shift in x direction
            y_shift (float): determine shift in y direction

        """
        self.x += x_shift
        self.y += y_shift
        self.update_rect()

    def update_rect(self):
        """
        Updates `rect` position by `x`, `y` values
        """
        self.rect.center = self.get_position()

    def _check_angle(self, angle):
        """
        Convert angle to <0; 360)

        Args:
            angle (float): angle to simplify

        Returns:
            float: simplify degrees

        """
        return math.fabs(angle % 360)

    def update_color(self, color):
        """
        Change `image` color
        """
        self.color = color
        self.color_changed = True

    def update_image(self):
        """
        Update image to match new attributes
        """
        if self.image_changed:
            self.image = pg.transform.rotate(self.original, self.rotation)
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=self.get_position())
        if ((self.color_changed or self.image_changed) and
                self.color is not None):
            self.image.fill(self.color)
        self.image_changed, self.color_changed = False, False

    def set_original(self, image):
        """
        Replace `original` and immediately create `image` from it

        Args:
            image (pg.Surface): new `original`
        """
        self.original = image
        self.image_changed = True
        self.update_image()

    def accelerate(self, angle, speed):
        """
        Accelerate in given angle by given speed

        Args:
            angle (float): angle of velocity vector to be add up
            speed (float): speed to be add

        """
        radians = math.radians(angle)
        self.dx += speed * math.cos(radians)
        self.dy += speed * math.sin(radians)

    def rotate_angle(self, degree):
        """
        Rotate image by `degree` degree and update it

        Args:
            degree (float): rotation size
        """
        self.rotation = self._check_angle(self.rotation + degree)
        self.image_changed = True
        self.update_image()

    def update(self):
        """
        Set new possition using velocities

        The `dy` value is subtracted instead of added. As a result, positive
        `dy` moves sprite up, instead of down.
        """
        self.x += self.dx
        self.y -= self.dy
        self.rect.center = self.get_position()
        if self.colide:
            self._check_position()
        self.update_image()

    def get_position(self):
        """
        Return current position
        """
        return (self.x, self.y)


class _FrameBasedSprite(_MovingSprite, metaclass=abc.ABCMeta):
    """
    Sprite calls each frame `make_changes` and that `kill` itself at the end

    `make_changes` method have to be overloaded

    Args:
        max_frames (int): determine how long does the life of the object will
            be, at the final frame, it `kill` itself
        img (:obj:`str` or :obj:`pygame.Surface`):
        position (:obj:`tuple`of :obj:`int`): ship's initial position

    Attributes:
        count (int): number specifying what frame is the curent one

    """

    def __init__(self, max_frames, img, position):
        super().__init__(img, position)
        self.max_frames = max_frames
        self.count = 0

    def update(self):
        self.count += 1
        if self.count >= self.max_frames:
            self.kill()
        else:
            self.make_changes(self.count)
            super().update()

    @abc.abstractmethod
    def make_changes(self, frames):
        """
        The class should changes in this method

        This method have to be overloaded.
        """
