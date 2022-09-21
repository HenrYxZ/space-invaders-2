import pyglet

from constants import *
from app import App, window


game_app = App()
window.push_handlers(game_app)


def update(dt):
    game_app.update(dt)


def main():
    pyglet.clock.schedule_interval(update, CLOCK_INTERVAL)
    pyglet.app.run()


if __name__ == '__main__':
    main()
