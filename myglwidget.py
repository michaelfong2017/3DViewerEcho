import sys
from PySide2 import QtCore, QtOpenGL
import moderngl as mgl
from model import *
from camera import Camera
from keyeventhandler import KeyEventHandler
from arcball import ArcBallUtil
from light import Light
from mesh import Mesh
from scene import Scene


class MyGLWidget(QtOpenGL.QGLWidget):
    # x_rotation_changed = QtCore.Signal(int)
    # y_rotation_changed = QtCore.Signal(int)
    # z_rotation_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAcceptDrops(True)

        self.delta_time = 40 # 40ms per frame
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateGL)
        self.timer.start(self.delta_time)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.mesh.destroy()
            sys.exit()
        else:
            KeyEventHandler().add_pressed_key(e.key())

    def keyReleaseEvent(self, e):
        KeyEventHandler().remove_pressed_key(e.key())

    # def mousePressEvent(self, e):
    #     super().mousePressEvent(e)
    #     print(f"QGLWidget coordinates: ({e.x()}, {e.y()})")
    #     if e.button() == QtCore.Qt.LeftButton:
    #         print("LeftButton is pressed")
    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.arc_ball.onClickLeftDown(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.arc_ball.onClickLeftUp()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.arc_ball.onDrag(event.x(), event.y())

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        self.arc_ball.Transform[3, :3] = (
            -self.arc_ball.Transform[:3, :3].T @ self.center
        )

        try:
            self.scene.render()
        except AttributeError:
            # Don't print this error message so that console is not flushed
            pass

    # In seconds
    def get_time(self):
        self.time = self.elapsed_timer.elapsed() * 0.001

    # Note: WIN_SIZE might not be accurate. sometimes 100x100.
    # https://www.youtube.com/watch?v=eJDIsFJN4OQ&ab_channel=CoderSpace
    def initializeGL(self):
        # window size
        self.WIN_SIZE = (self.width(), self.height())
        print(f"WIN_SIZE: {self.WIN_SIZE}")
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE) # look into or outside of view
        # Enable blending
        self.ctx.enable(mgl.BLEND) # how to render front and back objects. occulsion.
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
        # init arcball
        self.init_arcball() # mouse controls for rotating view
        # create an object to help track time
        self.time = 0
        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

    def init_arcball(self):
        self.arc_ball = ArcBallUtil(self.width(), self.height())
        bbmin = np.array([-1.0, -1.0, -1.0])
        bbmax = np.array([1.0, 1.0, 1.0])
        self.center = 0.5 * (bbmax + bbmin)
        self.scale = np.linalg.norm(bbmax - self.center)
        print(self.center, self.scale)
        self.arc_ball.Transform[:3, :3] /= self.scale
        self.arc_ball.Transform[3, :3] = -self.center / self.scale

    def paintGL(self):
        self.get_time()
        self.camera.update()
        self.render()

    def resizeGL(self, width, height):
        width = max(2, width)
        height = max(2, height)
        self.ctx.viewport = (0, 0, width, height)

        self.arc_ball = ArcBallUtil(width, height)
        # print(self.camera.position)
