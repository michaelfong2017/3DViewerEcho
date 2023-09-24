import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.glWidget = self.ui.openGLWidget
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start(40)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
