"""
There is definition of main function.
Also here is specified list of all posible states of program.
"""

from . import prepare, tools
from .states import title, select, controls, game, quit


def main():
    """Set initial state to control."""
    app = tools.Control(prepare.CAPTION)
    state_dict = {'TITLE': title.Title(),
                  'SELECT': select.Select(),
                  'CONTROLS': controls.Controls(),
                  'GAME': game.Game(),
                  'QUIT': quit.Quit()}

    app.state_machine.setup_states(state_dict, 'TITLE')
    app.main()
