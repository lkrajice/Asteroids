"""
Module with constants, initial settings and pygame initialization

Attributes:
    FPS (int): fps of the program
    SCREEN_SIZE (:obj:`tuple` of :obj:`int`): default screen sizes
    CENTER (:obj:`tuple` of :obj:`int`): center of the screen
    CAPTION (str): caption of the window
    BACKGROUND_COLOR (:obj:`tuple` of :obj:`int`): default background color
    SCREEN_RECT (pygame.Rect): screen rectangle object
    SLOW_FACTOR (int): ship slows its speed by `SLOW_FACTOR` percent each frame
    FONT_PATHS (:obj:`list` of :obj:`str`): filepaths to fonts
    MUSIC_PATHS (:obj:`list` of :obj:`str`): filepaths to music
    SFX (:obj:`list` of :obj:`str`): filepaths to sfx
    GTX (:obj:`list` of :obj:`pygame.Surface`): loaded imagex

"""

import pygame as pg
import os

from data import tools

FPS = 60
SCREEN_SIZE = (1600, 836)
CENTER = [x // 2 for x in SCREEN_SIZE]
CAPTION = 'Asteroids'
BACKGROUND_COLOR = (0, 0, 30)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
SLOW_FACTOR = 1

FONT_PATHS = None
MUSIC_PATHS = None
SFX = None
GTX = None

SHIP = {  #: initial settings of ship
        'lives': 4,
        'score': 0,
        'initial_angle': 90,
        'xy': SCREEN_RECT.center,
        'max_speed': 10,
        'acceleration': 0.25,
        'rotate_speed': 270,
        'slow_factor': SLOW_FACTOR / 100
}

SMOKE = {  #: initial settings of ship's smoke particles
        'size': (5, 5),
        'color': [255, 0, 0],
        'end_color': [255, 120, 0],
        'frames': 15,
        'speed': 4,
}
SMOKE['rgb_change_per_frame'] = [(x - y) / SMOKE['frames'] for x, y
                                 in zip(SMOKE['color'], SMOKE['end_color'])]

ASTEROIDS = {  #: initial settings of asteroids
        'level': 3,
}

LASER = {  #: initial settings of lasers
        'speed': 30,
        'frames': 50,
        'max': 4,
        'img': pg.Surface((7, 7))
}

BIG_UFO = {  #: initial settings of big ufo
        'speed': 10,
        'shots_per_second': 3,
}

SMALL_UFO = {  #: initial settings of small ufo
        'speed': 8,
        'shots_per_second': 2
}


def init_display():
    """
    Function that initialize pygame

    Initialize pygame modules, load resources, set icon, set window and plot
    loading screen.
    """
    global FONT_PATHS
    global MUSIC_PATHS
    global SFX
    global GTX

    pg.init()

    icon_path = os.path.join('resources', 'graphics', 'icon.png')
    pg.display.set_icon(pg.image.load(icon_path))
    _screen = pg.display.set_mode(SCREEN_SIZE, pg.DOUBLEBUF)

    # Resources
    FONT_PATHS = tools.load_all_fonts(os.path.join('resources', 'fonts'))
    MUSIC_PATHS = tools.load_all_music(os.path.join('resources', 'music'))
    SFX = tools.load_all_sfx(os.path.join('resources', 'sounds'))
    GTX = tools.load_all_gtx(os.path.join('resources', 'graphics'))

    _Y_OFFSET = (pg.display.Info().current_w - SCREEN_SIZE[0]) // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(_Y_OFFSET, 25)
    pg.display.set_caption(CAPTION)

    # 'Loading' screen
    font = pg.font.Font(FONT_PATHS['ARCADECLASSIC'], 150)
    _screen.fill(BACKGROUND_COLOR)
    _render = font.render('LOADING', 0, pg.Color('white'))
    _screen.blit(_render, _render.get_rect(center=SCREEN_RECT.center))
    pg.display.flip()
