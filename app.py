import pyglet


from constants import *
import resources
from ui import GameUI


window = pyglet.window.Window(
    WIDTH + UI_WIDTH, HEIGHT + UI_HEIGHT,
    caption="Space Invaders"
)
batch = pyglet.graphics.Batch()
background_group = pyglet.graphics.OrderedGroup(0)
foreground_group = pyglet.graphics.OrderedGroup(1)
ui_group = pyglet.graphics.OrderedGroup(3)


class App:
    def __init__(self):
        self.background = pyglet.sprite.Sprite(
            resources.background_tex,
            x=WIDTH//2, y=UI_HEIGHT+HEIGHT//2,
            batch=batch, group=background_group
        )
        self.background.scale = 0.5
        self.game_ui = GameUI(batch, ui_group)


@window.event
def on_draw():
    window.clear()
    batch.draw()
