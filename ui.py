import pyglet


from constants import *
from line_rectangle import LineRectangle
import resources


class WeaponBar(pyglet.shapes.Rectangle):
    def __init__(self, name, img, count, x, width, render_settings):
        batch, ui_group, front_group = render_settings
        super().__init__(
            x, 0, width, UI_HEIGHT,
            color=UI_COLOR, batch=batch, group=ui_group
        )
        label_size = (width - UI_HEIGHT) // 2
        self.label = pyglet.text.Label(
            name, x=x+label_size/2,  y=UI_HEIGHT/2,
            font_size=FONT_SIZE-1, color=TEXT_COLOR, bold=True,
            batch=batch, group=front_group,
            anchor_x='center', anchor_y='center'
        )
        w, h = img.width, img.height
        img_size = max(w, h)
        self.sprite = pyglet.sprite.Sprite(
            img, x=x+label_size+UI_HEIGHT/2, y=UI_HEIGHT/2,
            batch=batch, group=front_group
        )
        self.sprite.scale = (UI_HEIGHT * 0.75) / img_size
        self.count = pyglet.text.Label(
            str(count), x=x+3*label_size/2+UI_HEIGHT, y=UI_HEIGHT/2,
            font_size=FONT_SIZE-1, color=TEXT_COLOR, bold=True,
            batch=batch, group=front_group,
            anchor_x='center', anchor_y='center'
        )


class InfoLog(pyglet.shapes.Rectangle):
    def __init__(self, render_settings):
        batch, background_group, ui_group = render_settings
        x = WIDTH
        y = UI_HEIGHT
        width = UI_WIDTH
        height = HEIGHT
        super().__init__(
            x, y, width, height,
            color=UI_COLOR, batch=batch, group=background_group
        )
        self.resources = pyglet.text.Label(
            f"Resources: {MINE_RESOURCES}",
            x=WIDTH + UI_WIDTH // 2, y=400, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.money = pyglet.text.Label(
            f"Money: $0",
            x=WIDTH + UI_WIDTH // 2, y=350, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.level = pyglet.text.Label(
            f"Level: 1",
            x=WIDTH + UI_WIDTH // 2, y=450, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.time = pyglet.text.Label(
            f"Time: 0",
            x=WIDTH + UI_WIDTH // 2, y=300, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.lives = pyglet.text.Label(
            f"Lives: {PLAYER_HP}",
            x=WIDTH + UI_WIDTH // 2, y=250, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.buy_mode = pyglet.text.Label(
            "-- BUY MODE --",
            x=WIDTH + UI_WIDTH // 2, y=180, anchor_x='center',
            anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE-2, bold=True,
            batch=batch, group=ui_group
        )
        self.buy_mode.visible = False


class GameUI:
    def __init__(self, player, game, mine, render_settings):
        batch, _, front_group = render_settings
        self.player = player
        self.game = game
        self.mine = mine
        weapons = [
            ("Laser", resources.laser_tex, LASER_START_COUNT),
            ("Missile", resources.missile_tex, 0),
            ("Plasma", resources.plasma_tex, 0),
            ("Nuke", resources.nuke_tex, 0)
        ]
        self.weapons_ui = []
        self.weapon_bar_width = WINDOW_WIDTH // len(weapons)
        for i, weapon in enumerate(weapons):
            wb = WeaponBar(
                *weapon, i * self.weapon_bar_width, self.weapon_bar_width,
                render_settings
            )
            self.weapons_ui.append(wb)
        self.info_log = InfoLog(render_settings)
        self.selected_frame = LineRectangle(
            0, 0, UI_HEIGHT, UI_HEIGHT, 3, color=(0, 0, 0),
            batch=batch, group=front_group
        )
        self.change_selection(0)

    def change_selection(self, i):
        label_w = (self.weapon_bar_width - UI_HEIGHT) // 2
        self.selected_frame.position = (
            i * self.weapon_bar_width + label_w, 0
        )

    def update_count(self, i, new_count):
        self.weapons_ui[i].count.text = str(new_count)

    def update(self):
        self.info_log.resources.text = f"Resources: {self.mine.resources_left}"
        self.info_log.money.text = f"Money: ${self.game.money}"
        self.info_log.level.text = f"Level: {self.game.level}"
        self.info_log.time.text = f"Time: {int(self.game.time)}"
        self.info_log.lives.text = f"Lives: {self.player.hp}"
