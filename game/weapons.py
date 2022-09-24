import pyglet


from constants import *
import resources


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, direction, batch, group):
        super(Projectile, self).__init__(img, x, y, batch=batch, group=group)
        self.scale = SCALE
        self.direction = direction
        self.collision_dist = (2 * PROJECTILE_RADIUS) ** 2
        self.damage = 0
        self.dead = False

    # TODO: fix this
    def collides(self, entity):
        # collide at the middle of the enclosing cell
        other_x, other_y = entity.position
        other_x += entity.width // 2
        other_y += entity.height // 2
        if (
            (self.x - other_x) ** 2 + (self.y - other_y) ** 2 <=
            self.collision_dist
        ):
            return True
        return False

    def update(self, dt):
        self.y += self.direction * PROJECTILE_SPEED * dt


class Laser(Projectile):
    def __init__(self, x, y, batch, group):
        super(Laser, self).__init__(
            resources.laser_tex, x, y, NORMAL_DIRECTION, batch, group
        )
        self.damage = LASER_DAMAGE


class AlienLaser(Projectile):
    def __init__(self, x, y, batch, group):
        super(AlienLaser, self).__init__(
            resources.alien_laser_tex, x, y, OPPOSITE_DIRECTION, batch, group
        )
        self.damage = LASER_DAMAGE
