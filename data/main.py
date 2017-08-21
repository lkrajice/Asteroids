"""
Main function that start the program

Here is specified list of all posible states of program. These states preloads
during 'loading screen'.
"""

from data import prepare, tools
from data.states import title, select, controls, game, quit


def main():
    """
    Set initial state to control.

    Initialize display and set all game states, then run the core.
    """
    prepare.init_display()

    app = tools.Control(prepare.CAPTION)
    state_dict = {'TITLE': title.Title(),
                  'SELECT': select.Select(),
                  'CONTROLS': controls.Controls(),
                  'GAME': game.Game(),
                  'QUIT': quit.Quit()}

    app.state_machine.setup_states(state_dict, 'TITLE')
    app.main()
