from PySide2 import QtGui, QtUiTools, QtCore
from ui_mainwindow import Ui_MainWindow
from util import resource_path

from multiprocessing.pool import ThreadPool
import random
import time
import requests
import pickle
import blosc
import numpy as np
import base64

from formatconverter import dicom_to_array, pad4d
import PlaneReconstructionUtils
from matplotlib import pyplot
from PIL import Image
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datamanager import DataManager
from euler import eulerFromNormal, find_center_point


def process_frame(frame, frame_index):
    pickled_data = pickle.dumps(frame)
    compressed_data = blosc.compress(pickled_data)

    url = "http://localhost:8000/process_frame"
    headers = {"Content-Type": "application/octet-stream"}

    try:
        response = requests.post(url, data=compressed_data, headers=headers)

        if response.status_code == 200:
            compressed_data = response.content

            # Decompress the received data
            pickled_data = blosc.decompress(compressed_data)

            # Deserialize the pickled data to a NumPy array
            view_to_array_2d: dict = pickle.loads(pickled_data)

            with open(resource_path(f"pickle/{frame_index}.pickle"), "wb") as file:
                pickle.dump(view_to_array_2d, file)
        else:
            print("Error:", response.text)
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("process_frame response is not 200")
            dialog.label_2.setText("")
            dialog.exec_()
            return
    except:
        print("Loading pickle data...")
        ## UI dialog is not needed since it's already displayed during the normalize_dicom_array API call
        with open(resource_path(f"pickle/{frame_index}.pickle"), "rb") as file:
            view_to_array_2d = pickle.load(file)

    all_results = {}
    i = 0
    for view, array_2d in view_to_array_2d.items():
        # print("---------------------------------------------------------------")
        # print(view)
        pred_coords_raw = array_2d

        # print("Received: ", pred_coords_raw)

        st = time.perf_counter()

        try:

            # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
            # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
            # Note: You can modify time_index value to get plane visual from other time slices
            pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, normal = PlaneReconstructionUtils.FindVisualFromCoords(
                pred_coords_raw, frame, view
            )

            nx, ny, nz = normal[0], normal[1], normal[2]
            rx, ry, rz = eulerFromNormal(nx, ny, nz)
            # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

            points = [pred_coords_raw[i] for i in pred_mapped_coords_index]
            center_point = find_center_point(points)

            normalized_point = np.zeros(3)
            normalized_point[0] = center_point[0] / 213.0
            normalized_point[1] = center_point[1] / 213.0
            normalized_point[2] = center_point[2] / 213.0

            cx, cy, cz = normalized_point
            # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

            # Rotate Image
            pred_image, pred_rotated_coords = PlaneReconstructionUtils.HandleRotationsNumpy(pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, view)
   
            pred_image, pred_rotated_coords = PlaneReconstructionUtils.ViewSpecificRotations(pred_image, pred_rotated_coords, view)
            
            # Convert Image to PIL image
            pred_image = Image.fromarray(pred_image)
            pred_image = pred_image.convert("L")
            # pred_image.save(view + 'testing_pred.png')

            width, height = pred_image.size
            px = 1 / pyplot.rcParams['figure.dpi']
            pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
            pyplot.margins(x=0)
            pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
            pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
            pyplot.imshow(pred_image, cmap='gray')
            # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
            # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
            annotated_qimage = pyplot_to_qimage()

            et = time.perf_counter()
            print("Execution time: ", et - st)  # 7.5s on jerry's computer

            all_results.update({view: (pred_image, pred_rotated_coords, annotated_qimage, rx, ry, rz, cx, cy, cz)})

        except Exception as e:
            print(e)
            all_results.update({view: None})

        i += 1


    return frame_index, all_results, view_to_array_2d

def process_frame_with_known_landmarks(frame, frame_index, view_to_array_2d):
    all_results = {}
    i = 0
    for view, array_2d in view_to_array_2d.items():
        pred_coords_raw = array_2d

        st = time.perf_counter()

        try:
            # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
            # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
            # Note: You can modify time_index value to get plane visual from other time slices
            pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, normal = PlaneReconstructionUtils.FindVisualFromCoords(
                pred_coords_raw, frame, view)

            nx, ny, nz = normal[0], normal[1], normal[2]
            rx, ry, rz = eulerFromNormal(nx, ny, nz)
            # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

            points = [pred_coords_raw[i] for i in pred_mapped_coords_index]
            center_point = find_center_point(points)

            normalized_point = np.zeros(3)
            normalized_point[0] = center_point[0] / 213.0
            normalized_point[1] = center_point[1] / 213.0
            normalized_point[2] = center_point[2] / 213.0

            cx, cy, cz = normalized_point
            # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

            # Rotate Image
            pred_image, pred_rotated_coords = PlaneReconstructionUtils.HandleRotationsNumpy(pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, view)
   
            pred_image, pred_rotated_coords = PlaneReconstructionUtils.ViewSpecificRotations(pred_image, pred_rotated_coords, view)
            
            # Convert Imag eto PIL image
            pred_image = Image.fromarray(pred_image)
            pred_image = pred_image.convert("L")
            # pred_image.save(view + 'testing_pred.png')

            width, height = pred_image.size
            px = 1 / pyplot.rcParams['figure.dpi']
            pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
            pyplot.margins(x=0)
            pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
            pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
            pyplot.imshow(pred_image, cmap='gray')
            # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
            # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
            annotated_qimage = pyplot_to_qimage()

            et = time.perf_counter()
            print("Execution time: ", et - st)  # 7.5s on jerry's computer

            all_results.update({view: (pred_image, pred_rotated_coords, annotated_qimage, rx, ry, rz, cx, cy, cz)})

        except Exception as e:
            print(e)
            all_results.update({view: None})

        i += 1


    return frame_index, all_results

def thread_pool_test(frame, frame_index):
    r = random.randint(5, 7)
    time.sleep(r)
    print("Worker thread finishing")
    return (frame_index, r)

def process_dicom(analyze_all, filepath, ui: Ui_MainWindow, selected_frame_index):
    try:
        image4D, spacing4D = dicom_to_array(filepath)
    except FileNotFoundError as e:
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(resource_path("errordialog.ui"))
        ui_file.open(QtCore.QFile.ReadOnly)
        dialog = loader.load(ui_file)
        dialog.label.setText("Please select a valid filepath!")
        dialog.label_2.setText("")
        dialog.exec_()
        return
    
    display_video_info(ui)

    NUM_FRAMES = image4D.shape[0]

    ## ui loading bar
    # ui.progressBar.setValue(10)
    # ui.progressBar.setHidden(False)
    ##

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
    try:
        response = requests.post(url, data=serialized_data, headers=headers)

        if response.status_code == 200:
            compressed_data = response.content

            # Decompress the received data
            pickled_data = blosc.decompress(compressed_data)

            # Deserialize the pickled data to a NumPy array
            array_4d = pickle.loads(pickled_data)

            with open(resource_path(f"pickle/array_4d.pickle"), "wb") as file:
                pickle.dump(array_4d, file)
        else:
            print("Error:", response.text)
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("normalize_dicom_array response is not 200")
            dialog.label_2.setText("")
            dialog.exec_()
            return
    except:
        print("Loading pickle data...")
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(resource_path("errordialog.ui"))
        ui_file.open(QtCore.QFile.ReadOnly)
        dialog = loader.load(ui_file)
        dialog.label.setText("Server cannot be connected!")
        dialog.label_2.setText("Loading sample data...")
        dialog.exec_()
        with open(resource_path("pickle/array_4d.pickle"), "rb") as file:
            array_4d = pickle.load(file)
    # except requests.exceptions.ConnectionError as e:
    #     print(e)
    #     loader = QtUiTools.QUiLoader()
    #     ui_file = QtCore.QFile(resource_path("errordialog.ui"))
    #     ui_file.open(QtCore.QFile.ReadOnly)
    #     dialog = loader.load(ui_file)
    #     dialog.label.setText("Server connection error!")
    #     dialog.label_2.setText("Check server status & server url!")
    #     dialog.exec_()
    #     return

    data_4d_padded = array_4d

    # print(data_4d_padded)
    print(data_4d_padded.shape)

    DataManager().data_3d_padded_max_length = 213

    NUM_FRAMES = data_4d_padded.shape[0]
    print(f"NUM_FRAMES: {NUM_FRAMES}")

    pool = ThreadPool(21)
    results = []
    if selected_frame_index >= NUM_FRAMES:
        selected_frame_index = NUM_FRAMES - 1
    for i in range(NUM_FRAMES):
        # Analyze only one time frame
        if not analyze_all:
            if not i == selected_frame_index:
                continue
        # Analyze only one time frame END

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

        frame_index, all_results, view_to_array_2d = result.get()

        DataManager().update_pred_result(frame_index, all_results)

        results.append(result)

        is_first = True if not analyze_all or (analyze_all and i == 0) else False
        # Show the result without needing to move the horizontal slider
        if is_first:
            ui.horizontalSlider.setValue(0)
            ui.horizontalSlider.setValue(1)
            ui.horizontalSlider.setValue(i)

        # ## ui progress bar
        # if analyze_all:
        #     new_value = round(10 + (i + 1) * 90.0 / NUM_FRAMES)
        #     if new_value > 100:
        #         new_value = 100
        #     ui.progressBar.setValue(new_value)
        # else:
        #     ui.progressBar.setValue(20)
        ##

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    # print(results)

    # If analyze selected frame only, apply the landmark result to all other time frames as well
    if not analyze_all:
        assert not view_to_array_2d == None

        pool = ThreadPool(21)
        results = []
        for i in range(NUM_FRAMES):
            if i == selected_frame_index:
                continue

            data_3d_padded = data_4d_padded[i]

            result = pool.apply_async(
                process_frame_with_known_landmarks,
                args=(
                    data_3d_padded,
                    i,
                    view_to_array_2d,
                ),
            )

            frame_index, all_results = result.get()

            DataManager().update_pred_result(frame_index, all_results)
    
            results.append(result)

            ## ui progress bar
            # new_value = round(20 + (i + 1) * 80.0 / NUM_FRAMES)
            # if new_value > 100:
            #     new_value = 100
            # ui.progressBar.setValue(new_value)
            ##

        pool.close()
        pool.join()
        results = [r.get() for r in results]
        # print(results)

    ## ui
    # ui.progressBar.setHidden(True)
    ##

def display_video_info(ui: Ui_MainWindow):
    ui.label_16.setText(f"Video - Number of Frames: {DataManager().dicom_number_of_frames}")
    ui.label_15.setText(f"Video - Average Frame Time: {round(DataManager().dicom_average_frame_time_in_ms, 2)}ms")
    ui.label_9.setText(f"Video - FPS: {round(DataManager().dicom_fps, 2)}")
    ui.label_14.setText(f"Video - Total Duration: {round(DataManager().dicom_total_duration_in_s, 2)}s")

def pyplot_to_qimage():
    buf = io.BytesIO()
    pyplot.savefig(buf, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return QtGui.QImage.fromData(buf.getvalue())