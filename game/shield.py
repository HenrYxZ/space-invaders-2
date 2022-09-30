import pyglet


from constants import *
import resources


class Shield(pyglet.sprite.Sprite):
    def __init__(self, pos, batch, group):
        x = pos[0] * CELL_WIDTH
        y = pos[1] * CELL_HEIGHT + UI_HEIGHT
        super(Shield, self).__init__(
            resources.shield_tex, x, y,
            batch=batch, group=group, usage='static'
        )
        self.pos = pos
        self.scale = 0.25 * SCALE
        self.dead = False
