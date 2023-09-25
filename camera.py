import glm

FOV = 50
NEAR = 0.1
FAR = 100


class Camera:
    def __init__(self, app):
        self.app = app
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        # view matrix
        self.m_view = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, glm.vec3(0), self.up)

    def set_projection_matrix(self, aspect_ratio):
        self.m_proj = glm.perspective(glm.radians(FOV), aspect_ratio, NEAR, FAR)
        self.app.scene.shader_program["m_proj"].write(self.m_proj)
