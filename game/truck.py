import pyglet


from constants import *
import resources


class Truck(pyglet.sprite.Sprite):
    def __init__(self, batch, group):
        super(Truck, self).__init__(
            resources.truck_tex,
            x=25*CELL_SIZE, y=UI_HEIGHT, batch=batch, group=group
        )
        self.scale = 0.5
        self.cost = TRUCK_COST
        self._pos = 25
        self.accumulated_time = 0
        self.is_moving_left = True
        self.loading = False
        self.on_extracted = lambda: None
        self.on_loaded = lambda: None

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, i):
        self.x = i * CELL_SIZE
        self._pos = i

    def update(self, dt):
        self.accumulated_time += dt
        if self.accumulated_time >= TRUCK_TIME_TO_MOVE:
            self.accumulated_time = 0
            if self.pos == TRUCK_START_POS:
                if not self.loading:
                    # Start loading to factory
                    self.loading = True
                else:
                    # Finished loading to factory
                    self.loading = False
                    self.on_loaded()
                    self.image = resources.truck_l_tex
                    self.pos -= 1
                    self.is_moving_left = True
            elif self.pos == TRUCK_END_POS:
                if not self.loading:
                    self.loading = True
                else:
                    # change image and start moving left
                    self.loading = False
                    self.on_extracted()
                    self.image = resources.truck_tex
                    self.pos += 1
                    self.is_moving_left = False
            else:
                if self.is_moving_left:
                    self.pos -= 1
                else:
                    self.pos += 1
