import pyglet


pyglet.resource.path = ["./res"]
pyglet.resource.reindex()

background_tex = pyglet.resource.image("graphics/terra1920x1200.jpg")
background_tex.anchor_x = background_tex.width // 2
background_tex.anchor_y = background_tex.height // 2
