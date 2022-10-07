import pyglet

from constants import *
from app import App, window


game_app = App()
window.push_handlers(game_app)

@window.event
def on_draw():
    game_app.on_draw()


def main():
    pyglet.clock.schedule_interval(game_app.update, CLOCK_INTERVAL)
    pyglet.app.run()


if __name__ == '__main__':
    main()
