"""
First thing user see after loading screen.
"""


import pygame as pg

from . import widget_tools
from .. import prepare, tools, state_machine


ANY_KEY_Y = -100


class Title(state_machine._State):
    """
    Title screen.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = 'SELECT'
        self.timeout = 3
        self.header_text = widget_tools.SimpleText(
                'ARCADECLASSIC',
                200,
                prepare.CAPTION,
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
        self.header_text.draw(surface)
        self.any_key.draw(surface)

    def update(self, keys, now):
        self.any_key.update(now)
