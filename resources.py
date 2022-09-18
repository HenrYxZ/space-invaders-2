import pyglet


pyglet.resource.path = ["./res"]
pyglet.resource.reindex()

background_tex = pyglet.resource.image("graphics/terra1920x1200.jpg")
background_tex.anchor_x = background_tex.width // 2
background_tex.anchor_y = background_tex.height // 2

player_tex = pyglet.resource.image("graphics/Cañon.png")
truck_tex = pyglet.resource.image("graphics/CamioncitoDer.png")
truck_l_tex = pyglet.resource.image("graphics/CamioncitoIzq.png")
mine_tex = pyglet.resource.image("graphics/Cristales.png")
factory_tex = pyglet.resource.image("graphics/Fabrica.png")
enemy1_tex = pyglet.resource.image("graphics/nave1.png")
enemy2_tex = pyglet.resource.image("graphics/nave2.png")

enemy_images = [
    enemy1_tex, enemy2_tex
]

icon1 = pyglet.image.load("res/graphics/rocket-16.png")
icon2 = pyglet.image.load("res/graphics/rocket-32.png")
