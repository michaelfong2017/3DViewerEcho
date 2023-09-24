import sys
from PySide2 import QtCore, QtOpenGL
import moderngl as mgl
from model import Triangle


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
        print(f'QGLWidget coordinates: ({e.x()}, {e.y()})')
        if e.button() == QtCore.Qt.LeftButton:
            print("LeftButton is pressed")

    def initializeGL(self):
        self.ctx = mgl.create_context()

        self.scene = Triangle(self)

    def paintGL(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        self.scene.render()

    def resizeGL(self, width, height):
        width = max(2, width)
        height = max(2, height)
        self.ctx.viewport = (0, 0, width, height)

    # def free_resources(self):
    #     """Helper to clean up resources."""
    #     self.makeCurrent()
    #     glDeleteLists(self.shape1, 1)
