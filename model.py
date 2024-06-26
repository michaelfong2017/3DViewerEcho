import numpy as np
import glm
import moderngl as mgl


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), brightness=1.0):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.brightness = brightness
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # scale, note that the correct order is scale->rotate->translate and the order of matrix multiplication is from right to left
        m_model = glm.scale(m_model, self.scale)
        # m_model = glm.rotate(m_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.m_model = glm.rotate(self.m_model, 0.01, glm.vec3(0, 1, 0))
        self.texture.use()
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)


class Quad(BaseModel):
    def __init__(self, app, vao_name='quad', tex_pil=None, tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), brightness=1.0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, brightness)
        self.tex_pil = tex_pil
        self.on_init()

    def update(self):
        self.texture.use()
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        self.program["light.Ia"].write(self.app.light.Ia * self.brightness)

    def on_init(self):
        # texture
        if self.tex_pil == None:
            self.texture = self.app.mesh.texture.textures[self.tex_id]
        else:
            self.texture = self.app.mesh.texture.get_texture_from_pil(self.tex_pil)
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia * self.brightness)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)


class Line(BaseModel):
    def __init__(self, app, vao_name='line', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), color=(0.57, 0.0, 0.63, 1.0)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.color = glm.vec4(color)
        self.on_init()

    def update(self):
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        self.program["color"].write(self.color)

    def on_init(self):
        # mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        self.program["color"].write(self.color)

    def render(self):
        self.update()
        self.vao.render(mgl.LINES)