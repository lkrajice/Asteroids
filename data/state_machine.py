"""
Module that define general classes on witch application run

Classes in this module define program flow.
"""

import abc


class StateMachine:
    """
    A generic state machine

    Class is responsible for updating and drawing active state, fliping them
    and notify then about new events. Despite of the fact that `StateMachine`
    is used as top level controler of states, it can be also reused in lower
    levels. For example.: top level `StateMachine` contains state named
    'Select' witch contains another `StateMachine` with small states.

    Top-level machine is machine that is dirrectly connected to the `Control`
    class. Because of that, if top-level is done, program ends. But low-level
    is connected to 'controling state' (controling state is every state that
    contain another `StateMachine`), witch could be initiated by another
    low-level machine, or top-level machine. If low-level want higher machine
    to change its state, it is controling state's work to manage this request.
    Low-level machines uses `CommandState` to notify controling state about the
    request. Every controling state have to inmplement own way to proccess
    `CommandState`.

    Note:
        `__init__` method doesn't fully setup class. More information how to
        do it can be found in `setup_states` method.

    Attributes:
        quit (bool): if true, program ends
        done (bool): determine status of state tree. If top level is done,
            main loop ends. This doesn't work with low-level. See class
            description for details between top-level and low-level state
            machine.
        state_dict (:obj:`list` of :obj:`data.state_dict._State`): All
            states that this are avaible this state machine. Variable is
            defined in `setup_states`.
        state_name (str): name of active state. Variable is defined in
            `setup_states`.
        state (:obj:`data.state._State`): currently active state. Variable
            is defined in `setup_states`.

    """
    def __init__(self):
        self.quit = False
        self.done = False
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        """
        Set up the class

        Args:
            state_dict (:obj:`dict` of :obj:`data.state_machine._State`): dict
                that should contain all possible states for this state machine.
                All states should be already fully initialized.
            start_state (str): key from `state_dict` to state, that should be
                set to active first.

        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, now):
        """
        Update state and check for state's request

        State can request for application quit or to change state in actual
        level or higher level.

        Args:
            now (int): current time

        """
        self.now = now
        self.state.update(now)
        if self.state.quit:
            self.quit = True
        elif self.state.done:
            self.flip_state()

    def draw(self, surface):
        """
        Send draw request to active state.

        Args:
            surface (pygame.Surface): screen surface

        """
        self.state.draw(surface)

    def flip_state(self):
        """
        End or stop current state and active another one

        Also method keep some objects alive through cleanup and startup
        methods.
        """
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.now, persist)
        self.state.previous = previous

    def get_event(self, event):
        """
        Pass events down to current State

        Args:
            event (pygame.event.Event): event in pygame format

        """
        self.state.get_event(event)


class _State(abc.ABC):
    """
    Generic class for states

    `get_event and `update` must be overloaded in the childclass.

    Attributes:
        start_time (float): last time when state become active
        now (float): current_time
        done (bool): if set to True, state machine start next state, witch
            name have to be in `next`
        quit (bool): if set to True, application ands
        next (str): name of next state, that starts when `done` is True
        persist (:obj:`dict` of optional): dict of objects that need to stay
            alive

    """
    def __init__(self):
        self.start_time = 0.0
        self.now = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.persist = {}

    @abc.abstractmethod
    def get_event(self, event):
        """
        Processes events that were passed from the main event loop.

        Args:
            event (pygame.event.Event): event in pygame format

        """

    def startup(self, now, persistant):
        """
        Set start time and save variables that needs to stay alive

        Args:
            now (int): actual time
            persistant (:obj:`list` of optionals object): object that needed to
                stay alive

        """
        self.persist = persistant
        self.start_time = now

    def cleanup(self):
        """
        Reset state.done to False and send persistant object to state machine
        """
        self.done = False
        return self.persist

    @abc.abstractmethod
    def update(self, now):
        """
        Update function for state

        Args:
            now (int): current time

        """


class _ControlingState(_State):
    """
    Generic controling state class

    Class extends default `_State` class. It provides automated updating, event
    passing and notifying state machine to draw active state.
    """
    def __init__(self):
        """
        Regular init that additionaly add state machine

        Attributes:
            state_machine (StateMachine): low-level state machine

        """
        super().__init__()
        self.state_machine = StateMachine()

    def update(self, now):
        """
        Notify low-level state machine to update, the it checks for request

        Args:
            now (int): current time

        """
        self.state_machine.update(now)
        if self.state_machine.quit:
            self.quit = True
        elif self.state_machine.state.done:
            if isinstance(self.state_machine.state, CommandState):
                self.next = self.state_machine.state.require_higher_level_to
            self.done = True

    def draw(self, surface):
        """
        Send draw request to state machine

        Args:
            surface (pygame.Surface): screen surface

        """
        self.state_machine.draw(surface)

    def get_event(self, event):
        """
        Pass events to state machine

        Args:
            event (pygame.event.Event): event in pygame format

        """
        self.state_machine.get_event(event)


class CommandState(_State):
    """
    State used by lower-level state machine to commant higher-level machine

    This special type of state have automaticly set `done` property to True.
    All controling states controls if state that should be disabled (because of
    `done` property) is instance of this clas. If so, controling state end
    itself and set next state to `require_highter_level_to`. This is the only
    job, that this class do, so no need to implement 'draw', 'update' or
    'get_event' methods.
    """
    def __init__(self, require):
        """
        Set `done` to true and determine next state

        Args:
            require (str): name of state that will be set as active by higher
                state machine

        """
        super().__init__()
        self.done = True
        self.require_higher_level_to = require

    def draw(self, surface):
        pass

    def update(self, now):
        pass

    def get_event(self, event):
        pass
