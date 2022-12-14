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
laser_tex = pyglet.resource.image("graphics/disparo.png")
laser_tex.anchor_x = laser_tex.width / 2
laser_tex.anchor_y = laser_tex.height / 2
alien_laser_tex = pyglet.resource.image("graphics/disparo2.png")
alien_laser_tex.anchor_x = alien_laser_tex.width / 2
alien_laser_tex.anchor_y = alien_laser_tex.height / 2
shield_tex = pyglet.resource.image("graphics/Shield.png")
missile_tex = pyglet.resource.image("graphics/Misil.png")
missile_tex.anchor_x = missile_tex.width / 2
missile_tex.anchor_y = missile_tex.height / 2
plasma_tex = pyglet.resource.image("graphics/plasma.png")
plasma_tex.anchor_x = plasma_tex.width / 2
plasma_tex.anchor_y = plasma_tex.height / 2
nuke_tex = pyglet.resource.image("graphics/Nuke.png")
nuke_tex.anchor_x = nuke_tex.width / 2
nuke_tex.anchor_y = nuke_tex.height / 2

enemy_images = [
    enemy1_tex, enemy2_tex
]

icon1 = pyglet.image.load("res/graphics/rocket-16.png")
icon2 = pyglet.image.load("res/graphics/rocket-32.png")
