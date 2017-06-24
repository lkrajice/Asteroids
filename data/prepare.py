"""
Module contains dictionaries of resources and constants.
It also initializes pygame.
"""

import pygame as pg

import os
import time

from . import tools


pg.init()

FPS = 60
SCREEN_SIZE = (1600, 836)
CAPTION = 'Asteroids'
BACKGROUND_COLOR = (0, 0, 30)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_FONT_PATH = os.path.join('resources', 'fonts', 'ARCADECLASSIC.ttf')
HEADER_FONT = pg.font.Font(_FONT_PATH, 150)


# Initialization
_ICON_PATH = os.path.join('resources', 'graphics', 'icon.png')
_Y_OFFSET = (pg.display.Info().current_w - SCREEN_SIZE[0]) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(_Y_OFFSET, 25)
pg.display.set_caption(CAPTION)
pg.display.set_icon(pg.image.load(_ICON_PATH))
_screen = pg.display.set_mode(SCREEN_SIZE, pg.DOUBLEBUF)


# 'Loading' screen
_screen.fill(BACKGROUND_COLOR)
_render = HEADER_FONT.render('LOADING', 0, pg.Color('white'))
_screen.blit(_render, _render.get_rect(center=SCREEN_RECT.center))
pg.display.flip()

# Resources
FONT_PATHS = tools.load_all_fonts(os.path.join('resources', 'fonts'))
MUSIC_PATHS = tools.load_all_music(os.path.join('resources', 'music'))
SFX = tools.load_all_sfx(os.path.join('resources', 'sounds'))
GTX = tools.load_all_gtx(os.path.join('resources', 'graphics'))

_SHIP_SIZES = GTX['ship'].get_size()

# Settings
SHIP = {
        'lives': 4,
        'score': 0,
        'initial_angle': 90,
        'xy': SCREEN_RECT.center,
        'max_speed': 10,
        'acceleration': 0.25,
        'rotate_speed': 270,
}
# If calculated differently, max_speed will change. 'slow_factor' take care
# max speed by itself.
_SLOW_SPEED_FACTOR = 5
SHIP['slow_factor'] = 1 - (SHIP['acceleration'] /
                           (_SLOW_SPEED_FACTOR * SHIP['max_speed']))

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
