import pyglet


from constants import *


class WeaponBar(pyglet.shapes.Rectangle):
    def __init__(self, batch, group):
        width = WIDTH + UI_WIDTH
        height = UI_HEIGHT
        super().__init__(
            0, 0, width, height,
            color=UI_COLOR, batch=batch, group=group
        )
        self.weapons = []


class InfoLog(pyglet.shapes.Rectangle):
    def __init__(self, batch, group):
        x = WIDTH
        y = UI_HEIGHT
        width = UI_WIDTH
        height = HEIGHT
        super().__init__(
            x, y, width, height,
            color=UI_COLOR, batch=batch, group=group
        )


class GameUI:
    def __init__(self, batch, group):
        self.weapons_ui = WeaponBar(batch, group)
        self.info_log = InfoLog(batch, group)
