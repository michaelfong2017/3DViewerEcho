import sys
from PySide2 import QtCore, QtOpenGL
import moderngl as mgl


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
            sys.exit()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == QtCore.Qt.LeftButton:
            print("press")

    def initializeGL(self):
        self.ctx = mgl.create_context()

    def paintGL(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))

    def resizeGL(self, width, height):
        pass

    # def free_resources(self):
    #     """Helper to clean up resources."""
    #     self.makeCurrent()
    #     glDeleteLists(self.shape1, 1)
