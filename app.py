import pyglet
from pyglet.window import key
import random


from constants import *
from game import Enemy, Game, Factory, Laser, Missile, Mine, Nuke, Plasma, \
    Shield, Truck
from game_over_dialog import GameOverDialog
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
render_settings = (batch, background_group, ui_group)

WEAPONS_NUM_KEYS = {
    key._1: Laser,
    key._2: Missile,
    key._3: Plasma,
    key._4: Nuke
}
WEAPONS_ID = {
    Laser: LASER_ID,
    Missile: MISSILE_ID,
    Plasma: PLASMA_ID,
    Nuke: NUKE_ID
}
WEAPONS_COST = {
    Laser: LASER_PACK_COST,
    Missile: MISSILE_PACK_COST,
    Plasma: PLASMA_PACK_COST,
    Nuke: NUKE_PACK_COST
}
WEAPONS_PACK_UNITS = {
    Laser: LASER_PACK_UNITS,
    Missile: MISSILE_PACK_UNITS,
    Plasma: PLASMA_PACK_UNITS,
    Nuke: NUKE_PACK_UNITS
}


class App:
    def __init__(self):
        self.background = pyglet.sprite.Sprite(
            resources.background_tex,
            x=WIDTH//2, y=UI_HEIGHT+HEIGHT//2,
            batch=batch, group=background_group
        )
        self.background.scale = 0.588 * SCALE
        self.game = Game()
        self.player = Player(batch, foreground_group)
        self.factory = Factory(batch, foreground_group)
        self.mine = Mine(batch, foreground_group)
        self.game_ui = GameUI(
            self.player, self.game, self.mine, render_settings
        )
        self.trucks = [
            Truck(
                batch, foreground_group,
                self.mine.extract_resources,
                self.game.add_load
            )
        ]
        self.trucks_queue = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_queue = []
        self.shields = []
        self.highest_shield_positions = [
            SHIELD_START_ROW - 1 for _ in range(NUM_CELLS)
        ]
        self.timer = 0
        self.spawn_time = True     # Spawn only every two times
        self.current_weapon = Laser
        self._in_buy_mode = False
        self.in_dialog = False
        self.game_over_dialog = GameOverDialog(self.reset)
        window.push_handlers(self.player)

    def reset(self):
        self.game.reset()
        self.player.reset()
        self.factory.reset()
        self.mine.reset()
        # Delete trucks
        for entity in (
            self.trucks + self.bullets + self.enemy_bullets + self.enemies +
            self.shields
        ):
            entity.delete()
        self.trucks = [
            Truck(
                batch, foreground_group,
                self.mine.extract_resources,
                self.game.add_load
            )
        ]
        self.trucks_queue = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_queue = []
        self.shields = []
        self.highest_shield_positions = [
            SHIELD_START_ROW - 1 for _ in range(NUM_CELLS)
        ]
        self.timer = 0
        self.spawn_time = True  # Spawn only every two times
        self.current_weapon = Laser
        self._in_buy_mode = False
        self.in_dialog = False
        self.game_ui.reset()

    @property
    def in_buy_mode(self):
        return self._in_buy_mode

    @in_buy_mode.setter
    def in_buy_mode(self, value):
        self._in_buy_mode = value
        self.game_ui.info_log.buy_mode.visible = value

    def create_truck(self, _):
        new_truck = Truck(
            batch, foreground_group,
            self.mine.extract_resources, self.game.add_load
        )
        self.trucks.append(new_truck)

    def on_key_press(self, symbol, _):
        if self.in_dialog:
            self.game_over_dialog.on_key_press(symbol, _)
            return

        if symbol == key.SPACE:
            weapon_id = WEAPONS_ID[self.current_weapon]
            if self.player.weapons_count[weapon_id]:
                # Shoot cannon
                x = self.player.x + self.player.width / 2
                y = self.player.y + self.player.height
                bullet = self.current_weapon(x, y, batch, dynamic_group)
                self.bullets.append(bullet)
                self.player.weapons_count[weapon_id] -= 1
                self.game_ui.update_count(weapon_id)
        if symbol == key.UP:
            if self.game.money >= SHIELD_COST:
                self.game.money -= SHIELD_COST
                # Add shield
                i = self.player.pos
                new_j = self.highest_shield_positions[i] + 1
                if new_j < SHIELD_START_ROW + SHIELD_MAX_ROWS:
                    self.highest_shield_positions[i] = new_j
                    new_shield = Shield((i, new_j), batch, foreground_group)
                    self.shields.append(new_shield)
        if symbol == key.B:
            self.in_buy_mode = not self.in_buy_mode
        # Weapon selection
        if symbol in WEAPONS_NUM_KEYS.keys():
            if self.in_buy_mode:
                weapon = WEAPONS_NUM_KEYS[symbol]
                cost = WEAPONS_COST[weapon]
                units = WEAPONS_PACK_UNITS[weapon]
                weapon_id = WEAPONS_ID[weapon]
                if self.game.money >= cost:
                    self.game.money -= cost
                    self.player.weapons_count[weapon_id] += units
                    self.game_ui.update_count(weapon_id)
                self.in_buy_mode = False
            else:
                new_weapon = WEAPONS_NUM_KEYS[symbol]
                self.current_weapon = new_weapon
                self.game_ui.change_selection(WEAPONS_ID[new_weapon])
        # Buy truck
        if self.in_buy_mode and symbol == key._0 and not self.factory.dead:
            if self.game.money >= TRUCK_COST and len(self.trucks) < MAX_TRUCKS:
                self.game.money -= TRUCK_COST
                pyglet.clock.schedule_once(
                    self.create_truck, TRUCK_TIME_TO_MOVE
                )
                self.in_buy_mode = False

    def spawn_enemies(self):
        self.spawn_time = not self.spawn_time
        if not self.spawn_time:
            return
        # Run randoms for spawning, adding into a queue
        for lvl, spawn_prob in ENEMY_SPAWN_PROB[self.game.level].items():
            if random.random() <= spawn_prob:
                self.enemy_queue.append(lvl)
        # Dequeue enemies
        if self.enemy_queue:
            # Only spawn a new into the map when there's space
            if not self.enemies or self.enemies[-1].pos[0] >= ENEMY_CELLS_WIDTH:
                enemy_lvl = self.enemy_queue.pop(0)
                new_enemy = Enemy(
                    enemy_lvl, self.enemy_bullets, batch,
                    foreground_group, dynamic_group
                )
                self.enemies.append(new_enemy)

    def update_bullets(self, dt):
        # Player Bullets
        for bullet in self.bullets:
            bullet.update(dt)
            for enemy in self.enemies:
                if enemy.dead:
                    continue
                if bullet.collides(enemy):
                    if not isinstance(bullet, Nuke):
                        enemy.hp -= bullet.damage
                        if enemy.hp <= 0:
                            enemy.dead = True
                        bullet.dead = True
                    else:
                        # Nuke kills all enemies
                        for e in self.enemies:
                            e.dead = True
                        bullet.dead = True
                        break

        # Enemy Bullets
        for bullet in self.enemy_bullets:
            bullet.update(dt)
            # Collision with shields
            for shield in self.shields:
                if bullet.collides(shield):
                    self.highest_shield_positions[shield.pos[0]] -= 1
                    shield.dead = True
                    bullet.dead = True
                    continue
            # Collision with player
            if bullet.collides(self.player):
                self.player.hp -= bullet.damage
                if not self.player.hp:
                    self.in_dialog = True
                bullet.dead = True
                continue
            # Collision with trucks
            for truck in self.trucks:
                if bullet.collides(truck):
                    truck.dead = True
                    bullet.dead = True
            # Collision with factory
            if not self.factory.dead and bullet.collides(self.factory):
                self.factory.hp -= bullet.damage
                bullet.dead = True
                if not self.factory.hp:
                    self.factory.dead = True
                    self.factory.visible = False

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
        # Remove dead trucks
        dead_trucks = [truck for truck in self.trucks if truck.dead]
        for dead_truck in dead_trucks:
            self.trucks.remove(dead_truck)
            dead_truck.delete()
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
        # Remove dead enemy bullets
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

    def update(self, dt):
        if self.in_dialog:
            return

        self.game.update(dt)
        self.timer += dt
        # Update periodic things
        if self.timer >= TIME_UNIT:
            self.timer = 0
            # Update enemies
            for enemy in self.enemies:
                enemy.move()
            # Spawn new enemies into queue
            self.spawn_enemies()

        # Update trucks
        if not self.factory.dead:
            for truck in self.trucks:
                truck.update(dt)

        # Damage from bullets
        self.update_bullets(dt)

        self.cleanup_entities()

        self.game_ui.update()

    def on_draw(self):
        window.clear()
        batch.draw()
        if self.in_dialog:
            self.game_over_dialog.draw()
