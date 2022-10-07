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
        self.pos = (FACTORY_START_POS, FACTORY_CELLS_HEIGHT - 1)
        self.cells_wide = 3
        self.dead = False

    def reset(self):
        self.hp = FACTORY_HP
        self.dead = False
        self.visible = True
