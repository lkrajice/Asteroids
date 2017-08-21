"""
Top class and useful tools

Module contain Control class, that control program and information flow. In
this class is the main loop. Besides that other useful tools such as timer and
loading loading function can be found here.

Attributes:
    TIME_PER_UPDATE (int): Delay (in milliseconds) between updates during
        program. This variable specifies the FPS of the program.

"""

import os
import pygame as pg

from data import state_machine

TIME_PER_UPDATE = 16


class Control:
    """
    Top-level class controling pretty much everything

    Control is the top level class that control flow of the program. The class
    contain main loop. It notify states about events, update them and draw
    them.

    Args:
        caption (str): caption of the window

    Attributes:
        screen (pygame.Surface): screen of application
        done (bool): determine if program is done; stops the main loop
        clock (pygame.time.Clock): class to get the delay between calls
        fps (int): fps of the program
        now (int): time of updating states
        state_machine (state_machine.StateMachine): control class that notify
            all states
    """
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0  #: programs fps
        self.now = 0.0
        self.state_machine = state_machine.StateMachine()

    def update(self):
        """
        Notify EventManager to update active state.

        End main loop if StateMachine quit.
        """
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.now)
        if self.state_machine.quit or self.state_machine.done:
            self.done = True

    def draw(self):
        """
        Make StateMachine to notify active state to draw itself
        """
        if not self.state_machine.quit and not self.state_machine.done:
            self.state_machine.draw(self.screen)
            pg.display.flip()

    def event_loop(self):
        """
        Make StateMachine to notify active state about key events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state_machine.get_event(event)

    def main(self):
        """
        Main loop for entire program.

        Generate all action, update program more then once.
        """
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
                lag -= TIME_PER_UPDATE
            self.draw()


class Timer:
    """
    Very simple timer

    Timer call callback when delay is higher then given limit. Timer have to be
    initialized first. See `check_tick`.

    Note:
        `__init__` method doesn't fully initialize the class, see `check_tick`.
    Args:
        delay (int): minimal delay (in milliseconds) between callback calls.
        callback (function): specify a function of one argument. The
            argument (int) is the number of calls before.
        ticks (int): maximum callback calls. If `ticks` is set to -1, this
            mechanic is disabled. If `ticks` is set to 0, timer disable
            itself (see `check_tick`).
        init_callback (bool): if True, first `check_tick` also run the callback
            as if the timer was already initialized (see `check_ticks`).

    Attributes:
        tick_count (int): store number of previously called callbacks
        timer (int): time when last callback was used
        done (bool): determine if class is done or not

    """
    def __init__(self, delay, callback, ticks=-1, init_callback=False):
        self.delay = delay
        self.ticks = ticks
        self.tick_count = 0
        self.timer = None
        self.done = False
        self.init_callback = init_callback
        self.callback = callback

    def check_tick(self, now):
        """
        Check if time delay is sufficient to call the callback

        When first called, class initiate itself and doesn't call the callback.
        This behavior can be changed by `init_callback` argument in __init__.
        If delay between last call is big enought, callback is called. Callback
        is called always once even if delay is big enougt.

        Args:
            now (int): actual time

        """
        if self.ticks == 0:
            self.done = True
        elif not self.timer and not self.done:
            self.timer = now
            if self.init_callback:
                self.tick_count += 1
                self.callback(self.tick_count)
        elif not self.done and self.delay <= now - self.timer:
            self.tick_count += 1
            self.timer = now
            self.callback(self.tick_count)
            if self.tick_count >= self.ticks and self.ticks is not -1:
                self.done = True


def _gtx_value_fce(colorkey, fullpath):
    """
    Load image file by given path and turn it into pygame Surface

    If image doesn't have alpha, it is created with given `colorkey`.

    Args:
        colorkey (:obj:`list` of :obj:`int`): color to be transparent
        fullpath(str): path to image

    Returns:
        pygame.Surface: surface with enabled alpha

    """
    img = pg.image.load(fullpath)
    if img.get_alpha():
        return img.convert_alpha()
    else:
        return img.convert().set_colorkey(colorkey)


def _get_paths_with_filter(directory, accept, fce=None):
    """
    Return a dict of objects made using filepaths from specified directory

    Args:
        directory (str): specify directory where function search files
        accept (:obj:`list` of :obj:`str`): accepted filename extensions. If
            file without accepted extension is found, it is ignored.
        fce (function): function that takes filepath of accepted files.
            Function should proccess the filepath and return object, that is
            used as returned dictionary value. If `fce` is None, filepath is
            used as value.

    Returns:
        :obj:`dict`: use filename as key and by default filepath is used as
            value. It can by changed by `fce` argument. If no accepted file was
            found, return empty dict.

    """
    files = {}
    for f in os.listdir(directory):
        name, ext = os.path.splitext(f)
        if ext.lower() in accept:
            fullpath = os.path.join(directory, f)
            files[name] = fullpath if fce is None else fce(fullpath)
    return files


def load_all_fonts(directory, accept=('.ttf')):
    """
    Return filepath to fond files in specified directory

    The function is modification of `_get_paths_with_filter`. For more details
    see its documentation.
    """
    return _get_paths_with_filter(directory, accept)


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg')):
    """
    Return filepath to music files in specified directory

    The function is modification of `_get_paths_with_filter`. For more details
    see its documentation.
    """
    return _get_paths_with_filter(directory, accept)


def load_all_sfx(directory, accept=('.wav', '.mp3', '.ogg')):
    """
    Return filepath to sfx files in specified directory

    The function is modification of `_get_paths_with_filter`. For more details
    see its documentation.
    """
    return _get_paths_with_filter(directory,
                                  accept,
                                  fce=lambda x: pg.mixer.Sound(x))


def load_all_gtx(directory, accept=('.png'), colorkey=(255, 0, 255)):
    """
    Return directory of loaded images

    The function is modification of `_get_paths_with_filter`. For more details
    see its documentation. For more information about dict values see
    `_gtx_value_fce`.
    """
    return _get_paths_with_filter(directory,
                                  accept,
                                  fce=lambda x: _gtx_value_fce(colorkey, x))
