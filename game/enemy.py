import pyglet
import random


from constants import *
from game.weapons import AlienLaser
import resources


class Enemy(pyglet.sprite.Sprite):
    def __init__(self, level, bullet_list, batch, group, laser_group):
        img_idx = level % len(resources.enemy_images)
        super(Enemy, self).__init__(
            resources.enemy_images[img_idx],
            x=0, y=WINDOW_HEIGHT-ENEMY_CELLS_HEIGHT*CELL_HEIGHT,
            batch=batch, group=group
        )
        self.scale = SCALE
        self.hp = level
        self.dead = False
        self.shoot_probability = level / 20
        x, y = self.position
        x += CELL_WIDTH // 2
        self.shoot_position = (x, y)
        self._pos = (0, NUM_CELLS - ENEMY_CELLS_HEIGHT)
        self.cells_wide = 2
        self.is_moving_left = False
        self.bullet_list = bullet_list
        self.batch = batch
        self.laser_group = laser_group

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        i, j = value
        self.position = (i * CELL_WIDTH, j * CELL_HEIGHT + UI_HEIGHT)
        x, y = self.position
        x += CELL_WIDTH // 2
        self.shoot_position = (x, y)

    def shoot(self):
        x, y = self.shoot_position
        if random.random() < 0.5:
            x += CELL_WIDTH
        laser = AlienLaser(x, y, self.batch, self.laser_group)
        self.bullet_list.append(laser)

    def move(self):
        r = random.random()
        i, j = self.pos
        # Move
        if self.is_moving_left:
            if i > 0:
                self.pos = (i - 1, j)
            else:
                self.pos = (i, j - ENEMY_CELLS_HEIGHT)
                self.is_moving_left = False
        else:
            if i < NUM_CELLS - 2:
                self.pos = (i + 1, j)
            else:
                self.pos = (i, j - ENEMY_CELLS_HEIGHT)
                self.is_moving_left = True
        # Shoot
        if r <= self.shoot_probability:
            self.shoot()
