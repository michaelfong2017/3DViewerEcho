from PySide2 import QtGui
from ui_mainwindow import Ui_MainWindow

from multiprocessing.pool import ThreadPool
import random
import time
import requests
import pickle
import blosc
import numpy as np
import base64

from formatconverter import dicom_to_array, pad4d
from ReconstructPlane import FindVisualFromCoords, HandleRotations
from PIL import Image
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datamanager import DataManager


def process_frame(frame, frame_index):
    pickled_data = pickle.dumps(frame)
    compressed_data = blosc.compress(pickled_data)

    url = "http://localhost:8000/process_frame"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=compressed_data, headers=headers)

    if response.status_code == 200:
        compressed_data = response.content

        # Decompress the received data
        pickled_data = blosc.decompress(compressed_data)

        # Deserialize the pickled data to a NumPy array
        array_2d = pickle.loads(pickled_data)
    else:
        print("Error:", response.text)
        # TODO alert user
        return

    pred_coords_raw = array_2d

    print(pred_coords_raw)
    print(pred_coords_raw.shape)

    st = time.perf_counter()

    # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
    # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
    # Note: You can modify time_index value to get plane visual from other time slices
    pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(
        pred_coords_raw, frame
    )

    pred_image = Image.fromarray(pred_vs)
    pred_image = pred_image.convert("L")

    # Rotate the image into a "correct" orientation
    pred_image, pred_rotated_coords = HandleRotations(
        pred_image, pred_mapped_coords, pred_up, None
    )
    # pred_image.save(save_dir + filename[0] + '_pred.png')

    et = time.perf_counter()
    print("Execution time: ", et - st)  # 7.5s on jerry's computer

    return frame_index, pred_image, pred_rotated_coords

def thread_pool_test(frame, frame_index):
    r = random.randint(5, 7)
    time.sleep(r)
    print("Worker thread finishing")
    return (frame_index, r)

def process_dicom(filepath, ui: Ui_MainWindow):
    image4D, spacing4D = dicom_to_array(filepath)
    NUM_FRAMES = image4D.shape[0]

    # ui slider BEGIN
    ui.horizontalSlider.setMinimum(0)
    ui.horizontalSlider.setMaximum(NUM_FRAMES - 1)
    ui.label_12.setText("0")
    ui.label_13.setText(str(NUM_FRAMES - 1))
    # ui slider END

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
    else:
        print("Error:", response.text)
        # TODO alert user
        return

    data_4d_padded = array_4d

    print(data_4d_padded)
    print(data_4d_padded.shape)

    NUM_FRAMES = data_4d_padded.shape[0]
    print(f"NUM_FRAMES: {NUM_FRAMES}")

    pool = ThreadPool(21)
    results = []
    for i in range(NUM_FRAMES):
        data_3d_padded = data_4d_padded[i]
        if i == 0:
            print(data_3d_padded.shape)

        # results.append(pool.apply_async(thread_pool_test, args=(data_3d_padded,i)))

        result = pool.apply_async(
            process_frame,
            args=(
                data_3d_padded,
                i,
            ),
        )

        frame_index, pred_image, pred_rotated_coords = result.get()

        DataManager().update_pred_result(frame_index, pred_image, pred_rotated_coords)

        results.append(result)

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    print(results)

def pyplot_to_qimage(pyplot_figure):
    # Create a canvas and render the plot on it
    canvas = FigureCanvas(pyplot_figure)
    buffer = io.BytesIO()
    canvas.print_png(buffer)

    # Create QImage from the buffer
    buffer.seek(0)
    qimage = QtGui.QImage.fromData(buffer.getvalue())

    return qimage