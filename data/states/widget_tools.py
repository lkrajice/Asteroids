"""
Module contain useful classes and functions that states can use

Attributes:
    ANY_KEY_BLINK_TIME (int): delay in miliseconds between blinks

"""

import pygame as pg

from data import prepare, tools

ANY_KEY_BLINK_TIME = 350


class SimpleText:
    """
    Basic text class without any special functionalities

    Args:
        font (src): name of the font
        size (int): size of the text
        text (src): text
        position (:obj:`tuple` of :obj:`int`): center's position of the surface
        color (:obj:`tuple` of :obj:`int`): color of the text in rgb

    """
    def __init__(self, font, size, text,
                 position=prepare.SCREEN_RECT.center, color=(255, 255, 255)):
        self.font = font
        self.size = size
        self.text = text
        self.color = color
        self.position = position
        self.update_text()

    def update_text(self):
        """
        Update image and rectangle
        """
        self.image = render_font(self.font, self.size, self.text, self.color)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface):
        """
        Draw text

        Args:
            surface (pygame.Surface): screen surface

        """
        surface.blit(self.image, self.rect)


class AnyKey(SimpleText):
    """
    Blinking 'Press any key' text

    Text doesn't really blinks, it is moved out of the screen in one frame.

    Args:
        font (src): name of the font
        size (int): size of the text
        position (:obj:`tuple` of :obj:`int`): center's position of the surface
        color (:obj:`tuple` of :obj:`int`): color of the text in rgb

    Attributes:
        visible (bool): determine if text is visible right now
        timer (tools.Timer): timer calls callback every
            `ANY_KEY_BLINK_TIME`

    """
    def __init__(self, font, size, position, color=(255, 255, 255)):
        super().__init__(font, size, 'Press any key', position, color)
        self.visible = True
        self.timer = tools.Timer(ANY_KEY_BLINK_TIME, self.toggle)

    def update(self, now):
        """
        Check tick if enought time passed to toogle visibility

        Args:
            now (int): actual time

        """
        self.timer.check_tick(now)

    def toggle(self, tick_count):
        """
        Toggle visibility by moving text out of the screen.

        This method is called automaticaly by `timer`.

        Args:
            tick_count (int): number of how many times method was called -
                required arguments by timer

        """
        if self.visible:
            self.rect.move_ip(0, prepare.SCREEN_SIZE[1] + self.rect.height)
        else:
            self.rect.move_ip(0, -(prepare.SCREEN_SIZE[1] + self.rect.height))
        self.visible = not self.visible


class SimpleImage:
    """
    Generic image class

    Args:
        image (pygame.Surface): loaded image
        position (:obj:`tuple` of :obj:`int`): center's position of the surface

    """
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(center=position)

    def draw(self, surface):
        """
        Draw image
        """
        surface.blit(self.image, self.rect)


def change_pos(position, x, y):
    """
    Change position and return it

    Args:
        position (:obj:`tuple` of :obj:`int`): original position
        x (int): change in x dirction
        y (int): change in y dirction

    Returns:
        :obj:`tuple` of :obj:`int`

    """
    return (position[0] + x, position[1] + y)


def render_font(font, size, text, color=(255, 255, 255)):
    """
    Return surface with rendered font, size and message

    Args:
        font (src): name of the font
        size (int): size of the text
        text (src): text
        color (:obj:`tuple` of :obj:`int`): color of the text in rgb

    Returns:
        pygame.Surface

    """
    font = pg.font.Font(prepare.FONT_PATHS[font], size)
    return font.render(text, 1, color)
