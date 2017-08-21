"""
Module defining 'controls' screen

Attributes:
    ANY_KEY_Y (int): vertical distance between any_key's center and screen's
        mitbottom

"""

import pygame as pg

from data.states import widget_tools
from data import prepare, state_machine

ANY_KEY_Y = 100


class Controls(state_machine._State):
    """
    Keybord screen.

    Draw image that shows how to control the game. Also contain 'any key' text.

    Attributes:
        next (str): name of next state to be active when `done` is True
        keyboard (widget_tools.SimpleImage): image with controls
        any_key (widget_tools.AnyKey): blinking 'any key' text

    """
    def __init__(self):
        super().__init__()
        self.next = 'SELECT'
        self.keybord = widget_tools.SimpleImage(
                prepare.GTX['keyboard'],
                prepare.SCREEN_RECT.center
        )
        any_key_center = widget_tools.change_pos(
                prepare.SCREEN_RECT.midbottom,
                0,
                -ANY_KEY_Y
        )
        self.any_key = widget_tools.AnyKey(
                'ARCADECLASSIC',
                80,
                any_key_center,
        )

    def get_event(self, event):
        """
        If key press detected, done itself to start 'SELECT' state
        """
        self.done = event.type == pg.KEYDOWN

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_COLOR)
        self.keybord.draw(surface)
        self.any_key.draw(surface)

    def update(self, now):
        self.any_key.update(now)
