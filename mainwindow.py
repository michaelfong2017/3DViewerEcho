import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_mainwindow import Ui_MainWindow
import os
import threading
from dicomprocessor import process_dicom


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.import_dicom)

    def import_dicom(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File"),
            os.getcwd(),
            self.tr("DICOM File (*.dcm)"),
        )
        filepath = file[0]

        t1 = threading.Thread(target=process_dicom, args=(filepath,))
        t1.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
