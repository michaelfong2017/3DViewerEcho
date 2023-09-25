import glm
from keyeventhandler import KeyEventHandler
from PySide2 import QtCore

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01


class Camera:
    def __init__(self, app):
        self.app = app
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        # view matrix
        self.m_view = self.get_view_matrix()

    def update(self):
        self.move()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = KeyEventHandler().get_pressed_keys()
        if QtCore.Qt.Key_W in keys:
            self.position += self.forward * velocity
        if QtCore.Qt.Key_S in keys:
            self.position -= self.forward * velocity
        if QtCore.Qt.Key_A in keys:
            self.position -= self.right * velocity
        if QtCore.Qt.Key_D in keys:
            self.position += self.right * velocity
        if QtCore.Qt.Key_Q in keys:
            self.position += self.up * velocity
        if QtCore.Qt.Key_E in keys:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, glm.vec3(0), self.up)

    def set_projection_matrix(self, aspect_ratio):
        self.m_proj = glm.perspective(glm.radians(FOV), aspect_ratio, NEAR, FAR)
        self.app.scene.shader_program["m_proj"].write(self.m_proj)
