from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout


class ClickableQLabel(QLabel):
    def __int__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            width = self.pixmap().width()
            print("Pixmap width:", width)
            dialog = FullScreenDialog(self.pixmap())
            dialog.exec_()


class FullScreenDialog(QDialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowTitle("Cross Section")
        # self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)

        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        scaled_pixmap = pixmap.scaledToHeight(QApplication.desktop().screenGeometry().height() * 3.0 / 5.0, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        # print(f"scaled_pixmap: {scaled_pixmap.width()}, {scaled_pixmap.height()}")
        # print(f"self.label: {self.label.width()}, {self.label.height()}")
        # print(f"self: {self.width()}, {self.height()}")
        # print(f"layout: {layout.width()}, {layout.height()}")

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.close()
