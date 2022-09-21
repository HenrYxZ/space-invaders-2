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

    def collides(self, entity):
        # Use circular collider
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
    def __init__(self, x, y, direction, batch, group):
        super(Laser, self).__init__(
            resources.laser_tex, x, y, direction, batch, group
        )
