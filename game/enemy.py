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
            x=0, y=HEIGHT+UI_HEIGHT-3*CELL_SIZE, batch=batch, group=group
        )
        self.scale = SCALE
        self.hp = level
        self.dead = False
        self.shoot_probability = level / 20
        x, y = self.position
        x += self.width // 2
        self.shoot_position = (x, y)
        self._pos = (0, 25)
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
        self.position = (i * CELL_SIZE, j * CELL_SIZE + UI_HEIGHT)
        x, y = self.position
        x += self.width // 2
        self.shoot_position = (x, y)

    def shoot(self):
        x, y = self.shoot_position
        laser = AlienLaser(x, y, self.batch, self.laser_group)
        self.bullet_list.append(laser)

    def move(self):
        r = random.random()
        i, j = self.pos
        # Move
        if self.is_moving_left:
            if i == 0:
                self.pos = (i, j - 3)
                self.is_moving_left = False
            else:
                self.pos = (i - 2, j)
        else:
            if i >= NUM_CELLS - 3:
                self.pos = (i, j - 3)
                self.is_moving_left = True
            else:
                self.pos = (i + 2, j)
        # Shoot
        if r <= self.shoot_probability:
            self.shoot()
