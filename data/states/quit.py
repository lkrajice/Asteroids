"""
Implementation of special state `Quit`
"""

import pygame as pg

from data import state_machine


class Quit(state_machine._State):
    """
    State used by CommandState to quit the application

    This state does pretty much nothing except it set `quit` to True
    immediately. This cause chain reaction that quit the application.

    This state should by used by low-level `StateMachine`s `CommandState`.
    `CommandState` can simply request to activate this state if they want app
    to exit.

    Attributes:
        quit (bool): if True, program exits

    """
    def __init__(self):
        self.quit = True

    def get_event(self, event):
        pass

    def draw(self, surface):
        pass

    def update(self, now):
        """
        Quit the game's window to hide exiting proccess witch may look ugly
        """
        pg.display.quit()
