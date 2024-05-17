from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout, QPushButton


class ClickableQLabel(QLabel):
    def __int__(self):
        super().__init__()
        self._tag = ""

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            width = self.pixmap().width()
            print("Pixmap width:", width)

            cross_section = self.parent()
            view_button = cross_section.findChild(QPushButton, "pushButton_13")

            self.on_click()

            self.dialog = ViewDialog(self.pixmap(), view_button.text())
            self.dialog.show()


class ViewDialog(QDialog):
    def __init__(self, pixmap, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowFlags(QtCore.Qt.Window)

        self.PIXMAP_OCCUPY_RATIO = 4.0 / 5.0

        # Set the initial size of the dialog
        screen_width = QApplication.desktop().screenGeometry().width()
        screen_height = QApplication.desktop().screenGeometry().height()
        self.setMinimumSize(min(400, screen_width), min(300, screen_height))
        init_width = min(500, screen_width)
        init_height = min(500, screen_height)
        self.resize(init_width, init_height)

        self.pixmap = pixmap # Always use the original to avoid quality loss

        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        height = init_height * self.PIXMAP_OCCUPY_RATIO
        scaled_pixmap = pixmap.scaledToHeight(height, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        width = min(init_width * self.PIXMAP_OCCUPY_RATIO, scaled_pixmap.width())
        scaled_pixmap = scaled_pixmap.scaledToWidth(width, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.label.setPixmap(scaled_pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        # print(f"scaled_pixmap: {scaled_pixmap.width()}, {scaled_pixmap.height()}")
        # print(f"self.label: {self.label.width()}, {self.label.height()}")
        # print(f"self: {self.width()}, {self.height()}")
        # print(f"layout: {layout.width()}, {layout.height()}")

    def resizeEvent(self, event):
        # Handle the resize event here
        # print("Widget resized:", event.size())
        pixmap = self.pixmap

        height = event.size().height() * self.PIXMAP_OCCUPY_RATIO
        scaled_pixmap = pixmap.scaledToHeight(height, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        width = min(event.size().width() * self.PIXMAP_OCCUPY_RATIO, scaled_pixmap.width())
        scaled_pixmap = scaled_pixmap.scaledToWidth(width, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.label.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.close()
