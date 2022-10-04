from constants import *


class Game:
    def __init__(self):
        self.level = 1
        self.money = 70
        self.time = 0

    def update(self, dt):
        self.time += dt
        if self.time >= self.level * NEXT_LEVEL_TIME:
            self.level += 1

    def add_load(self, amount):
        self.money += amount
