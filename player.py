import pyglet


from constants import *
import resources


class Player(pyglet.sprite.Sprite):
    def __init__(self, batch, group):
        super(Player, self).__init__(
            resources.player_tex, x=WIDTH//2, y=CELL_SIZE*3+UI_HEIGHT,
            batch=batch, group=group
        )
        self.scale = SCALE
