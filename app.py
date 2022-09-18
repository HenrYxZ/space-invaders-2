import pyglet


from constants import *
from game import Game, Factory, Mine, Truck
from player import Player
import resources
from ui import GameUI


window = pyglet.window.Window(
    WIDTH + UI_WIDTH, HEIGHT + UI_HEIGHT,
    caption="Space Invaders"
)
window.set_icon(resources.icon1, resources.icon2)
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
        self.game = Game()
        self.game_ui = GameUI(batch, foreground_group)
        self.player = Player(batch, foreground_group)
        self.factory = Factory(batch, foreground_group)
        self.mine = Mine(batch, foreground_group)
        self.trucks = [
            Truck(
                batch, foreground_group,
                self.mine.extract_resources,
                self.game.add_load
            )
        ]
        self.resources_label = pyglet.text.Label(
            f"Resources: {self.mine.resources_left}",
            x=WIDTH+UI_WIDTH//2, y=400, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.money_label = pyglet.text.Label(
            f"Money: ${self.game.money}",
            x=WIDTH+UI_WIDTH//2, y=350, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.level_label = pyglet.text.Label(
            f"Level: ${self.game.level}",
            x=WIDTH+UI_WIDTH//2, y=450, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.time_label = pyglet.text.Label(
            f"Time: ${self.game.time:d}",
            x=WIDTH + UI_WIDTH // 2, y=300, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        window.push_handlers(self.player)

    def update(self, dt):
        self.game.update(dt)
        for truck in self.trucks:
            truck.update(dt)
        self.resources_label.text = f"Resources: {self.mine.resources_left}"
        self.money_label.text = f"Money: ${self.game.money}"
        self.level_label.text = f"Level: {self.game.level}"
        self.time_label.text = f"Time: {int(self.game.time)}"


@window.event
def on_draw():
    window.clear()
    batch.draw()
