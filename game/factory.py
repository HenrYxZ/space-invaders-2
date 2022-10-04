import pyglet


from constants import *
import resources


class Factory(pyglet.sprite.Sprite):
    def __init__(self, batch, group):
        super(Factory, self).__init__(
            resources.factory_tex, x=FACTORY_START_POS*CELL_WIDTH, y=UI_HEIGHT,
            batch=batch, group=group, usage='static'
        )
        self.scale = SCALE
        self.hp = FACTORY_HP
        self.pos = (FACTORY_START_POS, 0)
        self.cells_wide = 3
