"""
All fundamental clases are here.
Also contained some loading functions.
Here is the main loop.
"""

import os
import abc
import pygame as pg

from . import state_machine


TIME_PER_UPDATE = 16  # Milliseconds - little bit above 60 fps


class Control:
    """
    Top level class, that contain main loop -
    notify states about events, update them and draw them
    """
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

    def update(self):
        """
        Update active state.
        End program, if required by state.
        """
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now)
        if self.state_machine.state.quit:
            self.done = True

    def draw(self, interpolate):
        """
        Notify active state it should drow its content
        """
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen, interpolate)
            pg.display.flip()

    def event_loop(self):
        """
        Notify active state about events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            else:
                self.keys = pg.key.get_pressed()
            self.state_machine.get_event(event)

    def main(self):
        """
        This is main loop for entire program.
        If needed, update states more than once.
        """
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
                lag -= TIME_PER_UPDATE
            self.draw(lag/TIME_PER_UPDATE)


class Timer:
    """
    Very simple timer. It does not take care about how late it checks tick.
    """
    def __init__(self, delay, callback, ticks=-1):
        """
        Delay is given in milliseconds; ticks is a number of ticks the timer
        will make before setting self.done to True. Pass a value -1 to bypass.
        callback specify function of one argument (tick count), that is called
        when 'delay' passed, but it is not called automaticly - check_tick
        must be called.
        """
        self.delay = delay
        self.ticks = ticks
        self.tick_count = 0
        self.timer = None
        self.done = False
        self.callback=callback

    def check_tick(self, now):
        """
        Call calback if 'delay' time passed.
        Class setup when first called, in that case it always use callback.
        """
        if not self.timer:
            self.timer = now
            self.callback(self.tick_count)
        elif not self.done and now - self.timer > self.delay:
            self.tick_count += 1
            self.timer = now
            if self.ticks == self.tick_count:
                self.done = True
            self.callback(self.tick_count)


def _gtx_value_fce(colorkey, fullpath):
    """
    Load image from fullpath and return image.
    If image does not contain alpha, create alpha from colorkey
    """
    img = pg.image.load(fullpath)
    if img.get_alpha():
        return img.convert_alpha()
    else:
        return img.convert().set_colorkey(colorkey)


def _get_paths_with_filter(directory, accept, fce=None):
    """
    Returns a dictionary of paths to all files in given directory by default.
    accept specifies accepted filename extensions. All other extensions are
    ignored.
    fce specifies a function of one argument (full path to file) which returns
    value is used as dictionarys item value.
    """
    files = {}
    for f in os.listdir(directory):
        name, ext = os.path.splitext(f)
        if ext.lower() in accept:
            fullpath = os.path.join(directory, f)
            files[name] = fullpath if fce is None else fce(fullpath)
    return files


def load_all_fonts(directory, accept=('.ttf')):
    return _get_paths_with_filter(directory, accept)


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg')):
    """
    Returns a dictionary of paths to music files in given directory.
    Extensions that are not in accept are ignored.
    """
    return _get_paths_with_filter(directory, accept)


def load_all_sfx(directory, accept=('.wav', '.mp3', '.ogg')):
    return _get_paths_with_filter(directory,
                                  accept,
                                  fce=lambda x: pg.mixer.Sound(x))


def load_all_gtx(directory, accept=('.png'), colorkey=(255, 0, 255)):
    return _get_paths_with_filter(directory,
                                  accept,
                                  fce=lambda x: _gtx_value_fce(colorkey, x))
