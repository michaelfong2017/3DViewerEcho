from PySide2 import QtCore
from PySide2.QtWidgets import QLabel


class ClickableQLabel(QLabel):
    def __int__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            width = self.pixmap().width()
            print("Pixmap width:", width)
