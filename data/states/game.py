"""
Asteroids, the game itself

Attributes:
    BOTTOM_Y_SHIFT (int): bottom margin of score and lives
    SIDE_MARGIN (int): side margin of score and lives
    FONT_SIZE (int): font size of score
    SPACING (int): vertical spacing between score and lives
    SHIP_SPACING (int): horizontal spacinh between life icons

"""

import pygame as pg

from data.states import widget_tools
from data import prepare, state_machine
from data.components import ship, asteroids

BOTTOM_Y_SHIFT = 10
SIDE_MARGIN = 20
FONT_SIZE = 70
SPACING = 10
SHIP_SPACING = 30


class Game(state_machine._State):
    """
    The game state

    Attributes:
        end (bool): determine if player lost all lives
        asteroids (asteroids.AsteroidsGroup): sprite group that contain all
            asteroids in it. It also provide some extra method
        playerGroup (pygame.sprite.GroupSingle): group that holds ship
        health (HealthBar): class tracking healths and drawing them
        score (Score): simple class that draw current score

    """
    def __init__(self):
        super().__init__()
        self.end = False

        self.asteroids = asteroids.AsteroidsGroup()
        self.asteroids.next_level()
        self.playerGroup = pg.sprite.GroupSingle()
        self.health = HealthBar(prepare.SHIP['lives'])
        self.score = Score()
        self.spawn()

    def spawn(self):
        """
        Spawn the ship and consume one health
        """
        self.ship = ship.Ship()
        self.health.lost()
        self.playerGroup.add(self.ship)

    def get_event(self, event):
        """
        Circulate events to restart object or ship depending on `end` value
        """
        if self.end:
            self.restart.get_event(event)
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.ship.space_pressed()

    def draw(self, surface):
        """
        Draw all game's objects
        """
        surface.fill(prepare.BACKGROUND_COLOR)
        if not self.end:
            self.ship.draw(surface)
        self.asteroids.draw(surface)
        self.score.draw(surface)
        self.health.draw(surface)

    def update(self, now):
        """
        Check ship and health, start next level if needed and check colision
        """
        if self.playerGroup.__len__() == 0:
            if self.health.healths > 0:
                self.spawn()
            else:
                self.end = True
        else:
            if self.asteroids.__len__() == 0:
                self.asteroids.next_level()
            self.ship.update(now)
            self.asteroids.update()
            self.check_collide()

    def check_collide(self):
        """
        Check for collisions

        Add 100 score if asteroid was destroyed.
        """
        for asteroid in pg.sprite.groupcollide(
                self.asteroids,
                self.ship.ship_lasers,
                1,
                1):
            self.score.add_score(100)

        if not self.ship.immortal:
            pg.sprite.groupcollide(self.playerGroup, self.asteroids, 1, 0)


class Restart(state_machine._State):
    """
    Class that handle game over screen
    """
    pass


class HealthBar:
    """
    Health bar that holds number of lives and draw them

    Args:
        healths (int): initial number of healths. One health have to be lost
            because of spawning the ship

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
        Deincrement healths and remove one ship icon
        """
        self.positions = self.positions[1:]
        self.healths -= 1


class Score(widget_tools.SimpleText):
    """
    Class manage drawing and incrementing score

    `SimpleText` extension that keep track of score

    Args:
        score (int): current score

    """
    def __init__(self):
        self.score = 0
        position = (prepare.SCREEN_RECT.right - SIDE_MARGIN,
                    prepare.SCREEN_RECT.bottom - BOTTOM_Y_SHIFT)
        super().__init__('ARCADECLASSIC', FONT_SIZE, '0', position)
        self.update_text()

    def update_text(self):
        """
        Recreate image
        """
        self.text = 'Score {score}'.format(score=self.score)
        super().update_text()
        self.rect = self.image.get_rect(bottomright=self.position)

    def add_score(self, value):
        """
        Adds `value` total score and update text
        """
        self.score += value
        self.update_text()
