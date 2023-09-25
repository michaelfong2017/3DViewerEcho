import sys
from PySide2 import QtCore, QtOpenGL
import moderngl as mgl
from model import *
from camera import Camera


class MyGLWidget(QtOpenGL.QGLWidget):
    # x_rotation_changed = QtCore.Signal(int)
    # y_rotation_changed = QtCore.Signal(int)
    # z_rotation_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAcceptDrops(True)

    def keyPressEvent(self, e):
        print(e.key())
        if e.key() == QtCore.Qt.Key_Q:
            self.scene.destroy()
            sys.exit()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        print(f"QGLWidget coordinates: ({e.x()}, {e.y()})")
        if e.button() == QtCore.Qt.LeftButton:
            print("LeftButton is pressed")

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()

    # In seconds
    def get_time(self):
        self.time = self.elapsed_timer.elapsed() * 0.001

    def initializeGL(self):
        # create opengl context
        self.ctx = mgl.create_context()
        # create an object to help track time
        self.time = 0
        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        # camera
        self.camera = Camera(self)
        # scene
        self.scene = Cube(self)

    def paintGL(self):
        self.get_time()
        self.render()

    def resizeGL(self, width, height):
        width = max(2, width)
        height = max(2, height)
        self.ctx.viewport = (0, 0, width, height)

        self.WIN_SIZE = (width, height)
        print(f"WIN_SIZE: {self.WIN_SIZE}")
        self.aspect_ratio = self.WIN_SIZE[0] / self.WIN_SIZE[1]
        self.camera.set_projection_matrix(aspect_ratio=self.aspect_ratio)

    # def free_resources(self):
    #     """Helper to clean up resources."""
    #     self.makeCurrent()
    #     glDeleteLists(self.shape1, 1)
