"""
Asteroids - the game itself.
"""

import pygame as pg

from . import widget_tools
from .. import prepare, tools, state_machine
from ..components import ship, asteroids, ufo


BOTTOM_Y_SHIFT = 10
SIDE_MARGIN = 20
FONT_SIZE = 80
SPACING = 10
SHIP_SPACING = 50

class Game(state_machine._State):
    """
    The core of the game.
    """
    def __init__(self):
        state_machine._State.__init__(self)
        self.end = False

        self.asteroids = asteroids.AsteroidsGroup()
        self.asteroids.next_level()
        self.playerGroup = pg.sprite.GroupSingle()
        self.health = HealthBar(prepare.SHIP['lives'])

        self.score = Score()

    def spawn(self):
        """
        Spawn ship and consume one life.
        """
        self.ship = ship.Ship()
        self.health.lost()
        self.playerGroup.add(self.ship)

    def get_event(self, event):
        """
        Proccess events, if player ship is destroyed.
        If not, ship handle movement on its own.
        """
        if self.end:
            self.restart.get_event(event)
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.ship.space_pressed()

    def draw(self, surface, interpolate):
        surface.fill(prepare.BACKGROUND_COLOR)
        if not self.end:
            self.ship.draw(surface)
        self.asteroids.draw(surface)
        self.score.draw(surface)
        self.health.draw(surface)

    def update(self, keys, now):
        if self.playerGroup.__len__() == 0:
            print(self.health.healths)
            if self.health.healths > 0:
                self.spawn()
            else:
                self.end = True
        else:
            if self.asteroids.__len__() == 0:
                self.asteroids.next_level()
            self.ship.update(keys, now)
            self.asteroids.update()
            self.check_collide()

    def check_collide(self):
        """
        Check for collisions.
        """
        for asteroid in pg.sprite.groupcollide(
                self.asteroids,
                self.ship.ship_lasers,
                1,
                1):
            self.score.add_score(100)


        if not self.ship.immortal:
            for asteroid in pg.sprite.groupcollide(
                    self.playerGroup,
                    self.asteroids,
                    1,
                    0):
                pass


class PlayerGroup(pg.sprite.GroupSingle):
    def __init__(self):
        pg.sprite.GroupSingle.__init__()

    def update(self, keys, now):
        sprite.update(keys, now)

    def get_event(self, event):
        sprite.get_event(event)


class Restart(state_machine._State):
    """
    Class that handle game over screen.
    """
    pass


class HealthBar:
    """
    Draw ship icons. Include self.healths property that show remaining ships.
    """
    def __init__(self, healths):
        self.healths = healths
        self.image = prepare.GTX['ship_icon']

        y = prepare.SCREEN_SIZE[1] - BOTTOM_Y_SHIFT - FONT_SIZE - SPACING
        x = prepare.SCREEN_SIZE[0] - SIDE_MARGIN
        x_shift = - SHIP_SPACING - prepare.GTX['ship_icon'].get_size()[0]
        self.positions = [(x + i * x_shift, y) for i in range(self.healths)]
        self.positions = list(reversed(self.positions))

    def draw(self, surface):
        for position in self.positions:
            surface.blit(self.image, self.image.get_rect(bottomright=position))

    def lost(self):
        """
        Deincrement healths and remove one ship icon.
        """
        self.positions = self.positions[1:]
        self.healths -= 1


class Score(widget_tools.SimpleText):
    """
    This class show score.
    """
    def __init__(self):
        self.position = (prepare.SCREEN_RECT.right - SIDE_MARGIN,
                    prepare.SCREEN_RECT.bottom - BOTTOM_Y_SHIFT)
        self.score = 0
        widget_tools.SimpleText.__init__(self, 'ARCADECLASSIC', FONT_SIZE, '0')
        self.update_text()

    def update_text(self):
        self.text = 'Score {score}'.format(score=self.score)
        widget_tools.SimpleText.update_text(self)
        self.rect = self.image.get_rect(bottomright=self.position)

    def add_score(self, value):
        """
        Add to score value value and update text.
        """
        self.score += value
        self.update_text()
