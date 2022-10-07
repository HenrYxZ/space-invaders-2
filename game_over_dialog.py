import pyglet
from pyglet.window import key


from constants import *


class GameOverDialog:
    def __init__(self, on_reset):
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.on_reset = on_reset
        center_x = WIDTH / 2
        center_y = HEIGHT / 2 + UI_HEIGHT
        width = WIDTH // 3
        height = HEIGHT // 3
        self.back = pyglet.shapes.Rectangle(
            center_x - width // 2, center_y - height // 2, width, height,
            color=UI_COLOR, batch=self.batch, group=self.background
        )
        self.title = pyglet.text.Label(
            "GAME OVER", font_size=FONT_SIZE+2, bold=True, color=TEXT_COLOR,
            x=center_x, y=center_y+25, anchor_x='center', anchor_y='center',
            batch=self.batch, group=self.foreground
        )
        self.title = pyglet.text.Label(
            "Press ENTER to play again",
            font_size=FONT_SIZE-1, bold=True, color=TEXT_COLOR,
            x=center_x, y=center_y-50, anchor_x='center', anchor_y='center',
            batch=self.batch, group=self.foreground
        )

    def on_key_press(self, symbol, _):
        if symbol == key.ENTER or symbol == key.RETURN:
            self.on_reset()

    def draw(self):
        self.batch.draw()
