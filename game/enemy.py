import pyglet
import random


from constants import *
import resources


class Enemy(pyglet.sprite.Sprite):
    def __init__(self, level, batch, group):
        img_idx = level % len(resources.enemy_images)
        super(Enemy, self).__init__(
            resources.enemy_images[img_idx],
            x=0, y=HEIGHT+UI_HEIGHT-3*CELL_SIZE, batch=batch, group=group
        )
        self.scale = SCALE
        self.hp = level
        self.dead = False
        self.shoot_probability = level / 20
        self._pos = (0, 25)
        self.is_moving_left = False

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        i, j = value
        self.position = (i * CELL_SIZE, j * CELL_SIZE + UI_HEIGHT)

    def move(self):
        r = random.random()
        if r <= self.shoot_probability:
            self.shoot()
        i, j = self.pos
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

    def shoot(self):
        print(f"bang from {self.pos}")
