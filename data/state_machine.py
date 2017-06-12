"""
A state machine. Used for general program flow.
It takes care about requesting update or action of right states.
"""

import abc


class StateMachine:
    """
    A generic state machine.
    """
    def __init___(self):
        self.done = False
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        """
        Given a dictionary of states and a state to start in,
        creates the self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, keys, now):
        """
        Checks if a state is done or has called for a game quit.
        State is flipped if state is done and State.update is called.
        """
        self.now = now
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(keys, now)

    def draw(self, surface, interpolate):
        """
        Send draw request to state.
        """
        self.state.draw(surface, interpolate)

    def flip_state(self):
        """
        When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed.
        """
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.now, persist)
        self.state.previous = previous

    def get_event(self, event):
        """
        Pass events down to current State.
        """
        self.state.get_event(event)


class _State(abc.ABC):
    """
    Abstract class for States. All states should inherit from it.
    get_event and update must be overloaded in the childclass.
    The startup and cleanup methods need to be overloaded when there is data
    that must persist between States.
    """
    def __init__(self):
        self.start_time = 0.0
        self.now = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    @abc.abstractmethod  # get_event(self, event) {{{2
    def get_event(self, event):
        """
        Processes events that were passed from the main event loop.
        """

    def startup(self, now, persistant):
        """
        Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time.
        """
        self.persist = persistant
        self.start_time = now

    def cleanup(self):
        """
        Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False.
        """
        self.done = False
        return self.persist

    @abc.abstractmethod  # update(self, keys, now) {{{2
    def update(self, keys, now):
        """Update function for state."""
