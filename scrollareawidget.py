from PySide2.QtWidgets import QWidget
from clickableqlabel import ClickableQLabel
from datamanager import DataManager
from PySide2 import QtGui

class ScrollAreaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_width = 0

    def resizeEvent(self, event):
        # Handle the resize event here
        # print("Widget resized:", event.size())
        current_width = self.width()
        diff = current_width - self.previous_width
        if current_width == self.previous_width:
            return
        else:
            # print("Width has changed!")
            self.previous_width = current_width

        labels = self.find_labels(self)
        for label in labels:
            view = label.tag.split(",")[0]
            frame_index = int(label.tag.split(",")[1])
            degree = int(label.tag.split(",")[2])

            current_tab_index = self.parent().parent().parent().parent().currentIndex()
            view_analyze_all_tab = current_tab_index == 1
            if view_analyze_all_tab:
                all_results = DataManager().get_pred_result_analyze_all(frame_index)
            else:
                all_results = DataManager().get_pred_result(frame_index)
            ## TODO error handling
            for v, pred_result in all_results.items():
                if v == view:
                    _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

            pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
            ## error handling
            if pixmap:
                transform = QtGui.QTransform().rotate(degree)
                pixmap = pixmap.transformed(transform)

                resize_width = (event.size().width() - 18 - 12) / 3 # TODO change 3 to N
                resized_pixmap = pixmap.scaled(resize_width, resize_width)
                label.setPixmap(resized_pixmap)
                label.parent().setFixedWidth(resize_width)
                label.setFixedHeight(resize_width)
                label.show()

    def find_labels(self, widget):
        labels = []

        if isinstance(widget, ClickableQLabel):
            labels.append(widget)

        for child in widget.children():
            if isinstance(child, QWidget):
                labels.extend(self.find_labels(child))

        return labels