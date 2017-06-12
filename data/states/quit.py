"""
Use only if application should end.
"""

import pygame as pg

from .. import state_machine, prepare


class Quit(state_machine._State):
    """
    The only useful think what this does is that it set
    self.quit to True immediatly, that causes program to end.
    """
    def __init__(self):
        self.done = True
        self.quit = True

    def get_event(self, event):
        pass

    def draw(self, surface, interpolate):
        pass

    def update(self, keys, now):
        """
        Quit the game's window to hide ugly quiting proccess.
        """
        pg.display.quit()
