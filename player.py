import pyglet
from pyglet.window import key


from constants import *
import resources


class Player(pyglet.sprite.Sprite):
    def __init__(self, batch, group):
        super(Player, self).__init__(
            resources.player_tex, x=WIDTH//2, y=CELL_SIZE*3+UI_HEIGHT,
            batch=batch, group=group
        )
        self.scale = SCALE
        self._pos = NUM_CELLS // 2 - 1

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.x = value * CELL_SIZE

    def on_key_press(self, symbol, _):
        if symbol == key.LEFT:
            if self.pos > 0:
                self.pos -= 1
        elif symbol == key.RIGHT:
            if self.pos < NUM_CELLS - 1:
                self.pos += 1
