import abc
import math
import pygame as pg

from .. import prepare

ENERGY_LOSS = 0  # percent


class _MovingSprite(pg.sprite.Sprite, metaclass=abc.ABCMeta):
    """
    Abstract advanced sprite. It's able to tracks position, speed and do
    various kinds of calculations. It takes care about movement, rotation and
    interacting with sides of the sreen.
    """

    def __init__(self, img, position):
        pg.sprite.Sprite.__init__(self, [])
        self.colide = True
        self.colide_rotation = True
        self.evergy_loss = ENERGY_LOSS
        self.move_rect = prepare.SCREEN_RECT

        self.dx = 0
        self.dy = 0
        self.x = position[0]
        self.y = position[1]
        self.rotation = 0

        self.original = prepare.GTX[img] if isinstance(img, str) else img
        self.image = None
        self.rect = None
        self.color = None
        self.alpha = 255

        self.update_image()

    def _check_position(self):
        """
        Check, if object does not overrun allowed rectangle.
        If so, direction speed in which object overrun rect is decressed by
        ENERGY_LOSS percent and reversed.
        """
        # x direction
        if self.rect.right > self.move_rect.right and self.dx > 0:
            self.dx *= -(1 - ENERGY_LOSS / 100)
            self.rect.right = self.move_rect.right
        elif self.rect.left < self.move_rect.left and self.dx < 0:
            self.dx *= -(1 - ENERGY_LOSS / 100)
            self.rect.left = self.move_rect.left
        # y direction
        if self.rect.bottom > self.move_rect.bottom and self.dy < 0:
            self.dy *= -(1 - ENERGY_LOSS / 100)
            self.rect.bottom = self.move_rect.bottom
        elif self.rect.top < self.move_rect.top and self.dy > 0:
            self.dy *= -(1 - ENERGY_LOSS / 100)
            self.rect.top = self.move_rect.top

    def _check_angle(self, angle):
        """
        Convert angle to <0; 360> and return it.
        """
        return math.fabs(angle % 360)

    def update_image(self):
        """
        Update image by new properties.
        """
        if self.rotation is not 0:
            self.image = pg.transform.rotate(self.original, self.rotation)
        else:
            self.image = self.original.copy()
        if self.color is not None:
            self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.get_position())

    def set_original(self, image):
        """
        Update image and rectangle.
        """
        self.original = image
        self.update_image()

    def accelerate(self, angle, speed):
        """
        Accelerate in given direction by speed.
        """
        radians = math.radians(angle)
        self.dx += speed * math.cos(radians)
        self.dy += speed * math.sin(radians)

    def rotate_angle(self, degree):
        """
        Rotate image by degree degree and update it.
        """
        self.rotation = self._check_angle(self.rotation + degree)
        self.update_image()

    def update(self):
        self.x += self.dx
        self.y -= self.dy
        if self.colide:
            self._check_position()
        self.update_image()

    def get_position(self):
        '''
        Return current position.
        '''
        return self.x, self.y


class _FrameBasedSprite(_MovingSprite, metaclass=abc.ABCMeta):
    """
    Simple extension. When update is called max_frames times, Sprite kill
    itself.
    """

    def __init__(self, max_frames, img, position):
        _MovingSprite.__init__(self, img, position)
        self.max_frames = max_frames
        self.count = 0

    def update(self, *args):
        self.count += 1
        if self.count >= self.max_frames:
            self.kill()
        else:
            self.make_changes(self.count)
            _MovingSprite.update(self)

    @abc.abstractmethod  # make_changes(self, now, frames)
    def make_changes(self, frames):
        pass
