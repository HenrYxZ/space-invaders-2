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

    def extract_resources(self):
        if self.resources_left:
            amount = min(TRUCK_LOAD, self.resources_left)
            self.resources_left -= amount
            return amount

    def reset(self):
        self.resources_left = MINE_RESOURCES
