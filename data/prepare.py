"""
Module contains dictionaries of resources and constants.
It also initializes pygame.
"""

import pygame as pg
import os

from . import tools

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

# Settings
SHIP = {
        'lives': 4,
        'score': 0,
        'initial_angle': 90,
        'xy': SCREEN_RECT.center,
        'max_speed': 10,
        'acceleration': 0.25,
        'rotate_speed': 270,
        'slow_factor': 1 - SLOW_FACTOR / (100)
}

SMOKE = {
        'size': (5, 5),
        'color': [255, 0, 0],
        'end_color': [255, 120, 0],
        'frames': 15,
        'speed': 4,
}
SMOKE['rgb_change_per_frame'] = [(x - y) / SMOKE['frames'] for x, y
                                 in zip(SMOKE['color'], SMOKE['end_color'])]

ASTEROIDS = {
        'level': 3,
}

LASER = {
        'speed': 30,
        'frames': 50,
        'max': 4,
        'img': pg.Surface((7, 7))
}

BIG_UFO = {
        'speed': 10,
        'shots_per_second': 3,
}

SMALL_UFO = {
        'speed': 8,
        'shots_per_second': 2
}


def init_display():
    """
    Function will init pygame window and resources.
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
