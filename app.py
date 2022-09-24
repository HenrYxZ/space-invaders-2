import pyglet
from pyglet.window import key
import random


from constants import *
from game import Enemy, Game, Factory, Laser, Mine, Shield, Truck
from player import Player
import resources
from ui import GameUI


window = pyglet.window.Window(
    WINDOW_WIDTH, WINDOW_HEIGHT, caption="Space Invaders"
)
window.set_icon(resources.icon1, resources.icon2)
batch = pyglet.graphics.Batch()
background_group = pyglet.graphics.OrderedGroup(0)
foreground_group = pyglet.graphics.OrderedGroup(1)
dynamic_group = pyglet.graphics.OrderedGroup(2)
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
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_queue = []
        self.shields = []
        self.highest_shield_positions = [
            SHIELD_START_ROW - 1 for _ in range(NUM_CELLS)
        ]
        self.timer = 0
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
            f"Level: {self.game.level}",
            x=WIDTH+UI_WIDTH//2, y=450, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.time_label = pyglet.text.Label(
            f"Time: {int(self.game.time)}",
            x=WIDTH+UI_WIDTH//2, y=300, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        self.lives_label = pyglet.text.Label(
            f"Lives: {self.player.hp}",
            x=WIDTH+UI_WIDTH//2, y=250, anchor_x='center', anchor_y='center',
            color=TEXT_COLOR, font_size=FONT_SIZE, bold=True,
            batch=batch, group=ui_group
        )
        window.push_handlers(self.player)

    def on_key_press(self, symbol, _):
        if symbol == key.SPACE:
            # Shoot cannon
            x = self.player.x + self.player.width / 2
            y = self.player.y + self.player.height
            laser = Laser(x, y, batch, dynamic_group)
            self.bullets.append(laser)
        if symbol == key.UP:
            # Add shield
            i = self.player.pos
            new_j = self.highest_shield_positions[i] + 1
            if new_j < SHIELD_START_ROW + SHIELD_MAX_ROWS:
                self.highest_shield_positions[i] = new_j
                new_shield = Shield((i, new_j), batch, foreground_group)
                self.shields.append(new_shield)

    def update_bullets(self, dt):
        # Player Bullets
        for bullet in self.bullets:
            bullet.update(dt)
            for enemy in self.enemies:
                if enemy.dead:
                    continue
                if bullet.collides(enemy):
                    enemy.hp -= bullet.damage
                    if enemy.hp < 0:
                        enemy.dead = True
                    bullet.dead = True

        # Enemy Bullets
        for bullet in self.enemy_bullets:
            bullet.update(dt)
            # Collision with player
            if bullet.collides(self.player):
                self.player.hp -= bullet.damage
                print("player hit")
                if not self.player.hp:
                    print("GAME OVER")
                bullet.dead = True
            # Collision with shields
            for shield in self.shields:
                if bullet.collides(shield):
                    shield.dead = True
                    bullet.dead = True

    def cleanup_entities(self):
        # Remove dead enemies
        dead_enemies = [enemy for enemy in self.enemies if enemy.dead]
        for dead_enemy in dead_enemies:
            self.enemies.remove(dead_enemy)
            dead_enemy.delete()
        # Remove dead shields
        dead_shields = [shield for shield in self.shields if shield.dead]
        for dead_shield in dead_shields:
            self.shields.remove(dead_shield)
            dead_shield.delete()
        # Remove dead bullets
        dead_bullets = []
        for bullet in self.bullets:
            if bullet.dead:
                dead_bullets.append(bullet)
                continue
            if bullet.y > WINDOW_HEIGHT:
                bullet.dead = True
                dead_bullets.append(bullet)
        for dead_bullet in dead_bullets:
            self.bullets.remove(dead_bullet)
            dead_bullet.delete()
        dead_bullets = []
        for bullet in self.enemy_bullets:
            if bullet.dead:
                dead_bullets.append(bullet)
                continue
            if bullet.y < UI_HEIGHT:
                bullet.dead = True
                dead_bullets.append(bullet)
        for dead_bullet in dead_bullets:
            self.enemy_bullets.remove(dead_bullet)
            dead_bullet.delete()

    def update_labels(self):
        self.resources_label.text = f"Resources: {self.mine.resources_left}"
        self.money_label.text = f"Money: ${self.game.money}"
        self.level_label.text = f"Level: {self.game.level}"
        self.time_label.text = f"Time: {int(self.game.time)}"
        self.lives_label.text = f"Lives: {self.player.hp}"

    def update(self, dt):
        self.game.update(dt)
        self.timer += dt
        # Update periodic things
        if self.timer >= TIME_UNIT:
            self.timer = 0
            # Update enemies
            for enemy in self.enemies:
                enemy.move()
            # Spawn new enemies into queue
            for lvl, spawn_prob in ENEMY_SPAWN_PROB[self.game.level].items():
                if random.random() <= spawn_prob:
                    self.enemy_queue.append(lvl)
            # Dequeue enemies
            if self.enemy_queue:
                enemy_lvl = self.enemy_queue.pop(0)
                new_enemy = Enemy(
                    enemy_lvl, self.enemy_bullets, batch,
                    foreground_group, dynamic_group
                )
                self.enemies.append(new_enemy)

        # Update trucks
        for truck in self.trucks:
            truck.update(dt)

        # Damage from bullets
        self.update_bullets(dt)

        self.cleanup_entities()

        self.update_labels()


@window.event
def on_draw():
    window.clear()
    batch.draw()
