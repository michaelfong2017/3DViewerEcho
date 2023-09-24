import glm

FOV = 50
NEAR = 0.1
FAR = 100


class Camera:
    def __init__(self, app):
        self.app = app

    def set_projection_matrix(self, aspect_ratio):
        self.m_proj = glm.perspective(glm.radians(FOV), aspect_ratio, NEAR, FAR)
        self.app.scene.shader_program["m_proj"].write(self.m_proj)
