import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2 import QtCore
from ui_mainwindow import Ui_MainWindow
import os
from formatconverter import dicom_to_nrrd, pad4d
import threading
from multiprocessing.pool import ThreadPool
import random
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.import_dicom)

    def upload(self, frame):
        r = random.randint(5, 7)
        time.sleep(r)
        print("Worker thread finishing")
        return r

    def process_dicom(self, filepath):
        nrrd_data = dicom_to_nrrd(filepath)

        print(nrrd_data.shape)

        # pad the data to uniform shape. Pad entire 4d data for future use
        data_4d_padded, _, max_length = pad4d(nrrd_data)
        print(data_4d_padded.shape)

        NUM_FRAMES = data_4d_padded.shape[0]
        print(f"NUM_FRAMES: {NUM_FRAMES}")

        pool = ThreadPool(21)
        results = []
        for i in range(NUM_FRAMES):
            data_3d_padded = data_4d_padded[i]
            if i == 0:
                print(data_3d_padded.shape)

            results.append(pool.apply_async(self.upload, args=(data_3d_padded,)))

        pool.close()
        pool.join()
        results = [r.get() for r in results]
        print(results)

    def import_dicom(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File"),
            os.getcwd(),
            self.tr("DICOM File (*.dcm)"),
        )
        filepath = file[0]

        t1 = threading.Thread(target=self.process_dicom, args=(filepath,))
        t1.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
