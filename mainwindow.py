import sys
from PySide2 import QtGui, QtUiTools, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton
from ui_mainwindow import Ui_MainWindow
import os
import threading
from dicomprocessor import process_dicom, pyplot_to_qimage
from datamanager import DataManager
from matplotlib import pyplot, cm
from clickableqlabel import ClickableQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.import_dicom)
        self.ui.horizontalSlider.valueChanged.connect(self.frame_index_changed)
        self.clearFirstCrossSection()

    def frame_index_changed(self, slider_value):
        print(slider_value)

        frame_index: int = slider_value
        self.ui.label_10.setText(f"Selected time frame index: {frame_index}")

        all_results = DataManager().get_pred_result(frame_index)
        
        self.clearCrossSection()

        if not all_results == None:
            i = 0
            for view, pred_result in all_results.items():
                try:
                    pred_image, pred_rotated_coords = pred_result
                    width, height = pred_image.size
                    px = 1 / pyplot.rcParams['figure.dpi']
                    pyplot.figure(frame_index * len(all_results) + i, figsize=(width * px, height * px))
                    pyplot.margins(x=0)
                    pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
                    pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
                    pyplot.imshow(pred_image, cmap='gray')
                    pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
                    # pyplot.savefig(str(frame_index * len(all_results) + i) + '.png', bbox_inches='tight', pad_inches=0)
                    annotated_qimage = pyplot_to_qimage(pyplot.gcf())

                    self.addCrossSection(annotated_qimage, view)
                except Exception as e:
                    print(e)

                i = i + 1

    def import_dicom(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File"),
            os.getcwd(),
            self.tr("DICOM File (*.dcm)"),
        )
        filepath = file[0]

        t1 = threading.Thread(
            target=process_dicom,
            args=(
                filepath,
                self.ui,
            ),
        )
        t1.start()

    def addCrossSection(self, annotated_qimage, view):
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(ClickableQLabel)
        ui_file = QtCore.QFile("crosssection.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        cross_section = loader.load(ui_file)
        ui_file.close()

        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        label = cross_section.findChild(QLabel, "label_8")
        label.setPixmap(pixmap)
        label.show()

        view_button = cross_section.findChild(QPushButton, "pushButton_13")
        view_button.setText(view)

        self.ui.horizontalLayout_3.addWidget(cross_section)
        self.ui.scrollAreaWidgetContents_3.setMinimumWidth(self.ui.scrollAreaWidgetContents_3.minimumWidth() + annotated_qimage.width() + 6)

    def clearCrossSection(self):
        self.clearLayout(self.ui.horizontalLayout_3)
        self.ui.scrollAreaWidgetContents_3.setFixedWidth(500)
        self.ui.scrollAreaWidgetContents_3.setMinimumWidth(12)

    def clearFirstCrossSection(self):
        self.clearNestedLayout(self.ui.horizontalLayout_3)
        self.ui.scrollAreaWidgetContents_3.setFixedWidth(500)
        self.ui.scrollAreaWidgetContents_3.setMinimumWidth(12)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                item.widget().deleteLater()

    def clearNestedLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item is not None:
                    while item.count():
                        subitem = item.takeAt(0)
                        widget = subitem.widget()
                        if widget is not None:
                            widget.setParent(None)
                    layout.removeItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
