"""
Show controls to user.
"""

import pygame as pg

from . import widget_tools
from .. import prepare, tools, state_machine


ANY_KEY_Y = -100


class Controls(state_machine._State):
    """
    Keybord screen.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = 'SELECT'
        self.keybord = widget_tools.SimpleImage(
                prepare.GTX['keyboard'],
                prepare.SCREEN_RECT.center
        )
        any_key_center = widget_tools.change_pos(
                prepare.SCREEN_RECT.midbottom,
                0,
                ANY_KEY_Y
        )
        self.any_key = widget_tools.AnyKey(
                'ARCADECLASSIC',
                80,
                any_key_center,
        )

    def get_event(self, event):
        """
        Start next state after pressing key
        """
        self.done = event.type == pg.KEYDOWN

    def draw(self, surface, interpolate):
        surface.fill(prepare.BACKGROUND_COLOR)
        self.keybord.draw(surface)
        self.any_key.draw(surface)

    def update(self, keys, now):
        self.any_key.update(now)
