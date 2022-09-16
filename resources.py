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