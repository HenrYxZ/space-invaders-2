import pyglet

from constants import *
from app import App


game_app = App()


def update(dt):
    game_app.update(dt)


def main():
    pyglet.clock.schedule_interval(update, CLOCK_INTERVAL)
    pyglet.app.run()


if __name__ == '__main__':
    main()
