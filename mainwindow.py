import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2 import QtCore
from ui_mainwindow import Ui_MainWindow
import os
from formatconverter import dicom_to_array, pad4d
import threading
from multiprocessing.pool import ThreadPool
import random
import time
import requests
import pickle
import blosc
import numpy as np
import base64


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.import_dicom)

    def process_frame(self, frame, frame_index):
        pickled_data = pickle.dumps(frame)
        compressed_data = blosc.compress(pickled_data)

        url = "http://localhost:8000/process_frame"
        headers = {"Content-Type": "application/octet-stream"}
        response = requests.post(url, data=compressed_data, headers=headers)

        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Error:", response.text)
            # TODO alert user
            return
        return frame_index

    def thread_pool_test(self, frame, frame_index):
        r = random.randint(5, 7)
        time.sleep(r)
        print("Worker thread finishing")
        return (frame_index, r)

    def process_dicom(self, filepath):
        image4D, spacing4D = dicom_to_array(filepath)
        NUM_FRAMES = image4D.shape[0]

        print(image4D.shape)
        print(spacing4D.shape)

        compressed_data = []
        for i in range(NUM_FRAMES):
            pickled_image4D = pickle.dumps(image4D[i])
            compressed_image4D = blosc.compress(pickled_image4D)
            encoded_image4D = base64.b64encode(compressed_image4D)
            compressed_data.append(encoded_image4D)

        pickled_spacing4D = pickle.dumps(spacing4D)
        compressed_spacing4D = blosc.compress(pickled_spacing4D)
        encoded_spacing4D = base64.b64encode(compressed_spacing4D)
        compressed_data.append(encoded_spacing4D)

        serialized_data = b";".join(compressed_data)

        url = "http://localhost:8000/normalize_dicom_array"
        headers = {"Content-Type": "application/octet-stream"}
        response = requests.post(url, data=serialized_data, headers=headers)
        if response.status_code == 200:
            compressed_data = response.content

            # Decompress the received data
            pickled_data = blosc.decompress(compressed_data)

            # Deserialize the pickled data to a NumPy array
            array_4d = pickle.loads(pickled_data)

            # Process the deserialized array_4d as needed
            print("Array shape:", array_4d.shape)
            print("Array data:", array_4d)
        else:
            print("Error:", response.text)
            # TODO alert user
            return

        data_4d_padded = array_4d

        print(data_4d_padded.shape)

        NUM_FRAMES = data_4d_padded.shape[0]
        print(f"NUM_FRAMES: {NUM_FRAMES}")

        pool = ThreadPool(21)
        results = []
        for i in range(NUM_FRAMES):
            data_3d_padded = data_4d_padded[i]
            if i == 0:
                print(data_3d_padded.shape)

            # results.append(pool.apply_async(self.thread_pool_test, args=(data_3d_padded,i)))
            results.append(
                pool.apply_async(
                    self.process_frame,
                    args=(
                        data_3d_padded,
                        i,
                    ),
                )
            )

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
