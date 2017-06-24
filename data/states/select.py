"""
Game's menu.
"""

import pygame as pg

from . import widget_tools
from .. import prepare, tools, state_machine

HEADER_MARGIN_TOP = 150
OPTIONS_Y = 200
OPTIONS_FONT_SIZE = 100
OPTIONS_SPACING = 150
OPTIONS = ['PLAY', 'CONTROLS', 'QUIT']
COLOR_SELECTED = (255, 255, 0)


class Select(state_machine._State):
    """
    Show game's menu and take care of it.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = ''
        self.quit = False
        self.header = None
        self.state_machine = state_machine.StateMachine()

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

    def startup(self, now, persist):
        """
        Create substructure similar to top application structure.
        OPTIONS state is menu itself, other states can user acces via menu.
        CommandSubstate command Select state, that it shoud end and call
        another state.
        """
        state_dict = {'OPTIONS': Options(OPTIONS),
                      'PLAY': CommandSubstate('GAME'),
                      'CONTROLS': CommandSubstate('CONTROLS'),
                      'QUIT': CommandSubstate('QUIT')}
        self.state_machine.setup_states(state_dict, 'OPTIONS')

    def get_event(self, event):
        self.state_machine.get_event(event)

    def draw(self, surface, interpolate):
        surface.fill(prepare.BACKGROUND_COLOR)
        self.header.draw(surface)
        self.state_machine.draw(surface, interpolate)

    def update(self, keys, now):
        """
        If CommandSubstate request quit, state quit and start
        'require_higher_level_to' state.
        """
        if self.state_machine.state.quit:
            self.next = self.state_machine.state.require_higher_level_to
            self.done = True
        else:
            self.state_machine.update(keys, now)


class OptionItem(widget_tools.SimpleText):
    """
    Only difference is that OptionItem contains is_selected that
    change its color. Used when item is selected.
    """
    def __init__(self, title, y):
        widget_tools.SimpleText.__init__(
                self,
                'ARCADECLASSIC',
                80,
                title,
                widget_tools.change_pos(prepare.SCREEN_RECT.center, 0, y)
        )

    def is_selected(self, selected):
        """
        Colorize text to COLOR_SELECTED or white.
        """
        if selected:
            self.color = COLOR_SELECTED
        else:
            self.color = (255, 255, 255)
        self.update_text()


class Options(state_machine._State):
    """
    Menu manager. Contains all menu items. Manage colorizinig.
    """
    def __init__(self, options):
        state_machine._State.__init__(self)
        self.next = ''
        self.option_items = [OptionItem(x, index * OPTIONS_SPACING)
                             for index, x in enumerate(options)]
        self.active_index = 0
        self.option_items[self.active_index].is_selected(True)

    def set_highline(self, new_index):
        """
        Change item colors if needed.
        """
        if 0 <= new_index <= len(self.option_items):
            self.option_items[self.active_index].is_selected(False)
            self.active_index = new_index
            self.option_items[self.active_index].is_selected(True)

    def draw(self, surface, interpolate):
        for item in self.option_items:
            item.draw(surface)

    def update(self, keys, now):
        pass

    def get_event(self, event):
        new_index = self.active_index
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:  # enter
                self.next = self.option_items[self.active_index].text
                self.done = True
            elif event.key == pg.K_UP:
                new_index = max(0, self.active_index - 1)
            elif event.key == pg.K_DOWN:
                new_index = min(len(self.option_items) - 1,
                                self.active_index + 1)
            self.set_highline(new_index)


class CommandSubstate(state_machine._State):
    """
    Special state. It set self.quit to True which kill superior state.
    self.require_highter_level_to commands higher state, what state shoul
    take place.
    """
    def __init__(self, require):
        state_machine._State.__init__(self)
        self.quit = True
        self.require_higher_level_to = require

    def draw(self, surface, interpolate):
        pass

    def update(self, keys, now):
        pass

    def get_event(self, event):
        pass
