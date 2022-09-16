import pyglet


from constants import *
import resources


class Mine(pyglet.sprite.Sprite):
    def __init__(self, batch, group):
        super(Mine, self).__init__(
            resources.mine_tex, x=0, y=UI_HEIGHT,
            batch=batch, group=group, usage='static'
        )
        self.scale = SCALE
        self.resources_left = MINE_RESOURCES
