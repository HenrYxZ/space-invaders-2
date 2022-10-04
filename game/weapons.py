import pyglet


from constants import *
from player import Player
import resources


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, img, direction, x, y, batch, group):
        super(Projectile, self).__init__(img, x, y, batch=batch, group=group)
        self.scale = SCALE
        self.direction = direction
        self.damage = 0
        self.dead = False
        self.i = x // CELL_WIDTH
        self.speed = PROJECTILE_SPEED

    def collides(self, entity):
        # collide at the middle of the enclosing cell
        if isinstance(entity.pos, tuple):
            other_i, other_j = entity.pos
        else:
            other_i = entity.pos
            other_j = (
                PLAYER_ROW + PLAYER_CELLS_HEIGHT if isinstance(entity, Player)
                else 0
            )
        if other_i + entity.cells_wide > self.i >= other_i:
            y = self.y - UI_HEIGHT
            if self.direction > 0:
                if y >= other_j * CELL_HEIGHT + CELL_HEIGHT / 2:
                    return True
            else:
                if y <= other_j * CELL_HEIGHT:
                    return True
        return False

    def update(self, dt):
        self.y += self.direction * self.speed * dt


class AlienLaser(Projectile):
    def __init__(self, x, y, batch, group):
        super(AlienLaser, self).__init__(
            resources.alien_laser_tex, OPPOSITE_DIRECTION, x, y, batch, group
        )
        self.damage = LASER_DAMAGE


class Laser(Projectile):
    def __init__(self, x, y, batch, group):
        super(Laser, self).__init__(
            resources.laser_tex, NORMAL_DIRECTION, x, y, batch, group
        )
        self.damage = LASER_DAMAGE


class Missile(Projectile):
    def __init__(self, *args):
        super(Missile, self).__init__(
            resources.missile_tex, NORMAL_DIRECTION, *args
        )
        self.damage = MISSILE_DAMAGE


class Nuke(Projectile):
    def __init__(self, *args):
        super(Nuke, self).__init__(resources.nuke_tex, NORMAL_DIRECTION, *args)
        self.scale = 0.75
        self.speed = PROJECTILE_SPEED * 0.6


class Plasma(Projectile):
    def __init__(self, *args):
        super(Plasma, self).__init__(
            resources.plasma_tex, NORMAL_DIRECTION, *args
        )
        self.scale = 0.1
        self.damage = PLASMA_DAMAGE
