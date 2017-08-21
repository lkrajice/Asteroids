"""
Module defining game's main menu

Attributes:
    HEADER_MARGIN_TOP (int): distance between header center and screen center
    OPTIONS_FONT_SIZE (int): size of fonts of menu items
    OPTIONS_SPACING (int): spacing between menu items
    OPTIONS (:obj:`list` of :obj:`str`): list of menu items
    COLOR_SELECTED (:obj:`list` of :obj:`str`): color of selected item

"""

import pygame as pg

from data.states import widget_tools
from data import prepare, state_machine

HEADER_MARGIN_TOP = 150
OPTIONS_FONT_SIZE = 100
OPTIONS_SPACING = 150
OPTIONS = ['PLAY', 'CONTROLS', 'QUIT']
COLOR_SELECTED = (255, 255, 0)


class Select(state_machine._ControlingState):
    """
    Controling state for main menu

    Create low-level `StateMachine`. 'OPTIONS' state is menu itself, other
    states are just `CommandState` witch can be selected to activate by menu.

    When CommandState is active, this 'SELECT' state recognize that and set
    `done` to True, also set `next` according to command states's
    `require_higher_level_to`.
    """
    def startup(self, now, persist):
        """
        Create option state and subcommands
        """
        state_dict = {'OPTIONS': Options(OPTIONS),
                      'PLAY': state_machine.CommandState('GAME'),
                      'CONTROLS': state_machine.CommandState('CONTROLS'),
                      'QUIT': state_machine.CommandState('QUIT')}
        self.state_machine.setup_states(state_dict, 'OPTIONS')


class OptionItem(widget_tools.SimpleText):
    """
    Menu item

    `SimpleText` extension. It only manages changing color.

    Args:
        text (str): text of menu item
        y (int): y position, x is always center of the screen

    """
    def __init__(self, text, y):
        position = widget_tools.change_pos(prepare.SCREEN_RECT.center, 0, y)
        super().__init__('ARCADECLASSIC', 80, text, position)

    def is_selected(self, selected):
        """
        Set text color due to given status

        Args:
            selected (bool): given actual status

        """
        if selected:
            self.color = COLOR_SELECTED
        else:
            self.color = (255, 255, 255)
        self.update_text()


class Options(state_machine._State):
    """
    Main menu of the game

    Args:
        option (:obj:`list` of :obj:`str`): list of menu items

    Attributes:
        option_items (:obj:`list` of :obj:`OptionItem`): list of menu items
        active_index (int): index of selected menu item
        header (widget_tools.SimpleText): header

    """
    def __init__(self, options):
        super().__init__()
        self.option_items = [OptionItem(x, index * OPTIONS_SPACING)
                             for index, x in enumerate(options)]
        self.active_index = 0
        self.option_items[self.active_index].is_selected(True)
        header_center = widget_tools.change_pos(
                prepare.SCREEN_RECT.midtop,
                0,
                HEADER_MARGIN_TOP
        )
        self.header = widget_tools.SimpleText(
                'ARCADECLASSIC',
                200,
                prepare.CAPTION,
                header_center
        )

    def set_highline(self, new_index):
        """
        Change colors of previously active and currently active option item

        Args:
            new_index (int): index of new selected item

        """
        if 0 <= new_index <= len(self.option_items):
            self.option_items[self.active_index].is_selected(False)
            self.active_index = new_index
            self.option_items[self.active_index].is_selected(True)

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_COLOR)
        self.header.draw(surface)
        for item in self.option_items:
            item.draw(surface)

    def update(self, now):
        pass

    def get_event(self, event):
        """
        Set new active item according to user event.
        """
        new_index = self.active_index
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.next = self.option_items[self.active_index].text
                self.done = True
            elif event.key == pg.K_UP:
                new_index = max(0, self.active_index - 1)
            elif event.key == pg.K_DOWN:
                new_index = min(len(self.option_items) - 1,
                                self.active_index + 1)
            self.set_highline(new_index)
