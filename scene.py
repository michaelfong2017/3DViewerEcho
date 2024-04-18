from model import *
from collections import OrderedDict


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # add(Cube(app))
        # add(Cube(app, tex_id=1, pos=(-2.5, 0, 0), rot=(45, 0, 0), scale=(1, 2, 1)))
        # add(Cube(app, tex_id=2, pos=(2.5, 0, 0), rot=(0, 0, 45), scale=(1, 1, 2)))

        add(Line(app, pos=(1, 0, 0), color=(1, 0, 0, 1))) # x-axis
        add(Line(app, pos=(0, 1, 0), rot=(0, 0, 90), color=(0, 1, 0, 1))) # y-axis
        add(Line(app, pos=(0, 0, 1), rot=(0, 90, 0), color=(0, 0, 1, 1))) # z-axis
        add(Quad(app, tex_id="skybox", pos=(0.08, -0.03, 0.02), rot=(-94.75 - 90, -46.99, 50.57), brightness=15.0)) # A2C
        add(Quad(app, tex_id="skybox", pos=(-0.05, 0.01, 0.01), rot=(87.42 - 90, -2.68, -2.56), brightness=1.0)) # A4C
        add(Quad(app, tex_id="skybox", pos=(-0.01, -0.24, -0.05), rot=(-85.07 - 90, 45.1, -41.71), brightness=1.0)) # ALAX
        # add(Quad(app, tex_id="x=0", pos=(0, 0, 0), rot=(0, -90, 0), brightness=1.0)) # x=0
        # add(Quad(app, tex_id="y=0", pos=(0, 0, 0), rot=(0, 0, 0), brightness=1.0)) # y=0
        # add(Quad(app, tex_id="z=0", pos=(0, 0, 0), rot=(90, 0, 0), brightness=1.0)) # z=0
        add(Line(app, pos=(0, -1, -1)))
        add(Line(app, pos=(0, -1, 1)))
        add(Line(app, pos=(0, 1, -1)))
        add(Line(app, pos=(0, 1, 1)))
        add(Line(app, pos=(-1, -1, 0), rot=(0, 90, 0)))
        add(Line(app, pos=(-1, 1, 0), rot=(0, 90, 0)))
        add(Line(app, pos=(1, -1, 0), rot=(0, 90, 0)))
        add(Line(app, pos=(1, 1, 0), rot=(0, 90, 0)))
        add(Line(app, pos=(-1, 0, -1), rot=(0, 0, 90)))
        add(Line(app, pos=(-1, 0, 1), rot=(0, 0, 90)))
        add(Line(app, pos=(1, 0, -1), rot=(0, 0, 90)))
        add(Line(app, pos=(1, 0, 1), rot=(0, 0, 90)))

        # n, s = 80, 2
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

    def render(self):
        d = {}
        for obj in self.objects:
            transformed = self.app.camera.m_view * glm.vec4(obj.pos, 1.0)
            distance = glm.length(self.app.camera.position - glm.vec3(transformed))
            if d.get(distance):
                d[distance].append(obj)
            else:
                d[distance] = [obj]
        
        od = OrderedDict(sorted(d.items(), reverse=True))

        for distance, objs in od.items():
            for obj in objs:
                obj.render()