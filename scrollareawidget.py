from PySide2.QtWidgets import QWidget
from clickableqlabel import ClickableQLabel
from datamanager import DataManager
from PySide2 import QtGui

class ScrollAreaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_height = 0

    def resizeEvent(self, event):
        # Handle the resize event here
        # print("Widget resized:", event.size())
        current_height = self.height()
        diff = current_height - self.previous_height
        if current_height == self.previous_height:
            return
        else:
            # print("Height has changed!")
            self.previous_height = current_height

        labels = self.find_labels(self)
        for label in labels:
            view = label.tag.split(",")[0]
            frame_index = int(label.tag.split(",")[1])

            all_results = DataManager().get_pred_result(frame_index)
            ## TODO error handling
            for v, pred_result in all_results.items():
                if v == view:
                    _, _, annotated_qimage = pred_result

            minimum_width = self.minimumWidth()

            pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
            ## error handling
            if pixmap:
                resize_height = 240 + event.size().height() - 369
                resized_pixmap = pixmap.scaled(resize_height, resize_height)
                label.setPixmap(resized_pixmap)
                label.parent().setFixedWidth(resize_height)
                label.setFixedHeight(resize_height)
                label.show()
                self.setMinimumWidth(minimum_width + diff)
                self.setMaximumWidth(minimum_width + diff)

    def find_labels(self, widget):
        labels = []

        if isinstance(widget, ClickableQLabel):
            labels.append(widget)

        for child in widget.children():
            if isinstance(child, QWidget):
                labels.extend(self.find_labels(child))

        return labels