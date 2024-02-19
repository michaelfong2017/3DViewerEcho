import sys
from PySide2 import QtWidgets, QtCore, QtOpenGL
import moderngl
import numpy as np
from PIL import Image

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        # Create a ModernGL context
        self.ctx = moderngl.create_context()

        # Define the vertices for the lines
        vertices = np.array([
            -0.6, -0.6, 0.0, 1.0,
            0.6, -0.6, 0.0, 1.0,
            -0.6, 0.6, 0.0, 1.0,
            0.6, 0.6, 0.0, 1.0,
        ], dtype='f4')

        # Create a vertex buffer object (VBO)
        self.vbo = self.ctx.buffer(vertices)

        # Define the vertex shader code
        vertex_shader = '''
        #version 330
        uniform mat4 model;
        in vec4 in_vert;
        void main() {
            gl_Position = model * in_vert;
        }
        '''

        # Define the fragment shader code
        fragment_shader = '''
        #version 330
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red color
        }
        '''

        # Create a shader program
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # Create a vertex array object (VAO)
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, "4f", "in_vert")])

        # Bind the shader program
        self.prog['model'].write(np.eye(4, dtype='f4'))  # Set the model matrix

    def paintGL(self):
        # Clear the window
        self.ctx.clear()

        # Render the first line
        scale_matrix = np.eye(4, dtype='f4')
        self.prog['model'].write(scale_matrix)  # Reset the model matrix
        self.vao.render(moderngl.LINES, vertices=2)

        # Render the second line
        scale_matrix = np.eye(4, dtype='f4')
        scale_matrix[0, 0] = 0.5
        scale_matrix[1, 1] = 0.5
        self.prog['model'].write(scale_matrix)  # Reset the model matrix
        self.vao.render(moderngl.LINES, first=2, vertices=2)

        # Save the frame as a PNG image
        frame = self.grabFrameBuffer()
        image = Image.fromqpixmap(frame)
        image.save('test.png')

    def resizeGL(self, width, height):
        # Set the viewport
        self.ctx.viewport = (0, 0, self.width(), self.height())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the GL widget
        self.gl_widget = GLWidget()

        # Set the GL widget as the central widget
        self.setCentralWidget(self.gl_widget)

        # Set the window properties
        self.setWindowTitle("ModernGL with PySide2")
        self.setGeometry(100, 100, 800, 600)

        # Start the timer for continuous rendering
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.gl_widget.update)
        self.timer.start(16)  # 60 FPS

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())