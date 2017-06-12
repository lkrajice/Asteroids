"""
Here is some widgets that states may use or inherit from.
Also here is some useful functions.
"""

import pygame as pg

from .. import prepare, tools


ANY_KEY_BLINK_TIME = 350


class SimpleText:
    """
    Basic text surface without anz special functions.
    """
    def __init__(self, font, size, text, position=None, color=(255,255,255)):
        self.font = font
        self.size = size
        self.text = text
        self.color = color
        if position is not None:
            self.position = position
        self.update_text()

    def update_text(self):
        """
        Update image and rectangle.
        """
        self.image = render_font(self.font, self.size, self.text, self.color)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class AnyKey(SimpleText):
    """
    Blinking 'Press any key' text.
    """
    def __init__(self, font, size, center):
        SimpleText.__init__(self, font, size, 'Press any key', center)
        self.visible = True
        self.timer = tools.Timer(ANY_KEY_BLINK_TIME, self.toggle)

    def update(self, now):
        self.timer.check_tick(now)

    def toggle(self, tick_count):
        """
        Toggle visibility by moving text out of the screen.
        """
        if self.visible:
            self.rect.y += 2 * prepare.SCREEN_SIZE[1]
        else:
            self.rect.y -= 2 * prepare.SCREEN_SIZE[1]
        self.visible = not self.visible


class SimpleImage:
    """
    Basic image.
    Offer draw method.
    """
    def __init__(self, image, center):
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def change_pos(position, x, y):
    """
    Return changed position
    """
    return (position[0] + x, position[1] + y)


def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Return surface with rendered font, size
    and message.
    """
    font = pg.font.Font(prepare.FONT_PATHS[font], size)
    return font.render(msg, 1, color)
