from PySide2 import QtGui, QtUiTools, QtCore
from ui_mainwindow import Ui_MainWindow
from util import resource_path
import os

from multiprocessing.pool import ThreadPool
import random
import time
import requests
import pickle
import blosc
import numpy as np
import base64

import PlaneReconstructionUtils
from matplotlib import pyplot
from PIL import Image
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datamanager import DataManager, ModelType
from formatconverter import dicom_to_array
from euler import eulerFromNormal, find_center_point



class ProcessDicomThread(QtCore.QThread):
    finished = QtCore.Signal(object)
    ui_update = QtCore.Signal(object)
    def __init__(self, array_4d, ui: Ui_MainWindow, selected_frame_index, use_five_frames):
        super().__init__()
        print("init ProcessDicomThread")
        self._is_running = True
        self.array_4d = array_4d
        self.ui = ui
        self.selected_frame_index = selected_frame_index
        self.use_five_frames = use_five_frames

        ## if not analyze_all, store array_4d for future use by analyze_all
        DataManager().data_4d_padded = array_4d

    def stop(self):
        self._is_running = False

    def run(self):
        print("run ProcessDicomThread")
        results = self.process_dicom(self.array_4d, self.ui, self.selected_frame_index, self.use_five_frames)
        # The only case that the results is None is when this thread is interrupted during one/five frame(s) analysis
        if not results == None:
            self.finished.emit(results)

    def process_dicom(self, array_4d, ui: Ui_MainWindow, selected_frame_index, use_five_frames):
        data_4d_padded = array_4d

        # print(data_4d_padded)
        print(data_4d_padded.shape)

        DataManager().data_3d_padded_max_length = data_4d_padded.shape[1]

        NUM_FRAMES = data_4d_padded.shape[0]
        print(f"NUM_FRAMES: {NUM_FRAMES}")

        if selected_frame_index >= NUM_FRAMES:
            selected_frame_index = NUM_FRAMES - 1

        if (selected_frame_index == -1):
            selected_frame_index = int(NUM_FRAMES / 2)

        if use_five_frames:
            five_indexes: list = self.select_five_indexes(NUM_FRAMES, selected_frame_index)

        DataManager().clear_pred_results()
        DataManager().clear_center_images()

        def reset_ui(ui):
            ui.gridWidget.clearAllItems(ui.gridWidget)
            ui.label_23.setText("")

        self.ui_update.emit((reset_ui, ui))

        pool = ThreadPool(21)
        results = []

        if use_five_frames:
            print('5 frames')
            five_frames = np.array([data_4d_padded[frame_index] for frame_index in five_indexes])
            data_3d_padded = data_4d_padded[selected_frame_index]
            print("data3d: ", data_3d_padded.shape)

            result = pool.apply_async(
                process_five_frames,
                args=(
                    data_3d_padded,
                    selected_frame_index,
                    five_frames,
                    five_indexes,
                ),
            )

            frame_index, all_results, view_to_array_2d, all_center_images = result.get()

            # if not self._is_running:
            #     pool.close()
            #     pool.join()
            #     results = [r.get() for r in results]
            #     return results
            
            DataManager().update_pred_result(frame_index, all_results)
            DataManager().update_center_images(frame_index, all_center_images)

            results.append(result)

            # Show the result without needing to move the horizontal slider
            def move_slider(ui, frame_index):
                ui.horizontalSlider.setValue(0)
                ui.horizontalSlider.setValue(1)
                ui.horizontalSlider.setValue(frame_index)
            self.ui_update.emit((move_slider, ui, frame_index))

            ## ui progress bar
            new_value = 20
            def update_progress_bar(ui):
                ui.progressBar.setValue(new_value)
            self.ui_update.emit((update_progress_bar, ui))
            ## END

        else: # single frame

            data_3d_padded = data_4d_padded[selected_frame_index]
            print("data3d: ", data_3d_padded.shape)

            result = pool.apply_async(
                process_frame,
                args=(
                    data_3d_padded,
                    selected_frame_index
                ),
            )

            # Returned frame_index must be the same as the originally passed selected_frame_index
            frame_index, all_results, view_to_array_2d, all_center_images = result.get()

            DataManager().update_pred_result(frame_index, all_results)
            DataManager().update_center_images(frame_index, all_center_images)

            results.append(result)

            # Show the result without needing to move the horizontal slider
            def move_slider(ui, frame_index):
                ui.horizontalSlider.setValue(0)
                ui.horizontalSlider.setValue(1)
                ui.horizontalSlider.setValue(frame_index)
            self.ui_update.emit((move_slider, ui, frame_index))

            ## ui progress bar
            new_value = 20
            def update_progress_bar(ui):
                ui.progressBar.setValue(new_value)
            self.ui_update.emit((update_progress_bar, ui))
            ## END

        pool.close()
        pool.join()
        results = [r.get() for r in results]
        # print(results)

        # If analyze selected frame only, apply the landmark result to all other time frames as well
        assert not view_to_array_2d == None

        pool = ThreadPool(21)
        results = []
        for i in range(NUM_FRAMES):
            if i == selected_frame_index:
                continue

            data_3d_padded = data_4d_padded[i]

            result = pool.apply_async(
                process_frame_with_known_matrix,
                # process_frame_with_known_landmarks,
                args=(
                    data_3d_padded,
                    i,
                    view_to_array_2d,
                ),
            )

            frame_index, all_results, all_center_images = result.get()

            if not self._is_running:
                pool.close()
                pool.join()
                return None

            DataManager().update_pred_result(frame_index, all_results)
            DataManager().update_center_images(frame_index, all_center_images)
    
            results.append(result)

            ## ui progress bar
            new_value = round(20 + (i + 1) * 80.0 / NUM_FRAMES)
            if new_value > 100:
                new_value = 100
            def update_progress_bar(ui):
                ui.progressBar.setValue(new_value)
            self.ui_update.emit((update_progress_bar, ui))
            ## END

        pool.close()
        pool.join()
        results = [r.get() for r in results]
            # print(results)

        ## ui, ui progress bar
        def update_progress_bar_and_analyze_button(ui):
            ui.progressBar.setHidden(True)
            ui.pushButton_11.setEnabled(True)
        self.ui_update.emit((update_progress_bar_and_analyze_button, ui))
        ## END
        return results

    def select_five_indexes(self, num_frames, selected_frame_index, mode='consecutive'):

        if selected_frame_index < 0 or selected_frame_index >= num_frames:
            raise Exception("Input Error: selected_frame_index must be >=0 and < num_frames")
        N = 5
        if num_frames < N:
            return list(range(num_frames))
        
        if mode == 'consecutive':
            selected = [selected_frame_index]
            max_num_left = selected_frame_index
            max_num_right = num_frames - 1 - selected_frame_index

            num_left = int(N / 2)
            num_right = int(N / 2)

            if max_num_left < num_left:
                num_right = num_right + (num_left - max_num_left)
                num_left = max_num_left
            elif max_num_right < num_right:
                num_left = num_left + (num_right - max_num_right)
                num_right = max_num_right

            for i in range(num_left):
                selected.append(selected_frame_index - 1 - i)
            for i in range(num_right):
                selected.append(selected_frame_index + 1 + i)

            return sorted(selected)

        elif mode == 'randomized':
            all_indices = list(range(num_frames))
            return sorted(random.sample(all_indices, N))

        else:
            raise ValueError("Unknown mode. Use 'consecutive' or 'randomized'")

class SendDicomThread(QtCore.QThread):
    finished = QtCore.Signal(object)
    ui_update = QtCore.Signal(object)
    def __init__(self, serialized_data, ui):
        super().__init__()
        print("init SendDicomThread")
        self._is_running = True
        self.serialized_data = serialized_data
        self.ui = ui

    def stop(self):
        self._is_running = False

    def run(self):
        print("run SendDicomThread")
        array_4d = self.send_dicom(self.serialized_data, self.ui)
        if self._is_running:
            self.finished.emit(array_4d)

    def send_dicom(self, serialized_data, ui):
        base_url = DataManager().server_base_url
        if not base_url.endswith("/"):
            base_url = base_url + "/"
        url = f"{base_url}normalize_dicom_array"
        headers = {"Content-Type": "application/octet-stream"}
        try:
            response = requests.post(url, data=serialized_data, headers=headers)

            def set_video_info_title(ui):
                ui.label_17.setText(f"DICOM File (Video) Info:")
                # Display video info
                ui.label_36.setText(f"File: {DataManager().filename}")
                ui.label_16.setText(f"Number of Frames: {DataManager().dicom_number_of_frames}")
                ui.label_15.setText(f"Average Frame Time: {round(DataManager().dicom_average_frame_time_in_ms, 2)}ms")
                ui.label_9.setText(f"FPS: {round(DataManager().dicom_fps, 2)}")
                ui.label_14.setText(f"Total Duration: {round(DataManager().dicom_total_duration_in_s, 2)}s")
                # END
            self.ui_update.emit((set_video_info_title, ui))

            if response.status_code == 200:
                compressed_data = response.content

                # Decompress the received data
                pickled_data = blosc.decompress(compressed_data)

                # Deserialize the pickled data to a NumPy array
                array_4d = pickle.loads(pickled_data)

                with open(resource_path(os.path.join("pickle", "array_4d.pickle")), "wb") as file:
                    pickle.dump(array_4d, file)
            else:
                print("Error:", response.text)
                def alert_response_not_200(ui):
                    loader = QtUiTools.QUiLoader()
                    ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                    ui_file.open(QtCore.QFile.ReadOnly)
                    dialog = loader.load(ui_file)
                    dialog.label.setText("normalize_dicom_array response is not 200")
                    dialog.label_2.setText("")
                    dialog.exec_()
                self.ui_update.emit((alert_response_not_200, ui))
                return
        except:
            try:
                with open(resource_path(os.path.join("pickle", "array_4d.pickle")), "rb") as file:
                    array_4d = pickle.load(file)
                    print("Loading pickle data...")
                    def alert_use_sample_data(ui):
                        loader = QtUiTools.QUiLoader()
                        ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                        ui_file.open(QtCore.QFile.ReadOnly)
                        dialog = loader.load(ui_file)
                        dialog.setWindowTitle("Notification")
                        dialog.label.setText("Server cannot be connected!")
                        dialog.label_2.setText("Loading sample data...")
                        dialog.exec_()
                        ui.label_17.setText(f"(Using Sample Data) DICOM File (Video) Info:")
                        # Display video info
                        ui.label_36.setText(f"File: Sample Data")
                        ui.label_16.setText(f"Number of Frames: {DataManager().dicom_number_of_frames}")
                        ui.label_15.setText(f"Average Frame Time: {round(DataManager().dicom_average_frame_time_in_ms, 2)}ms")
                        ui.label_9.setText(f"FPS: {round(DataManager().dicom_fps, 2)}")
                        ui.label_14.setText(f"Total Duration: {round(DataManager().dicom_total_duration_in_s, 2)}s")
                        # END
                    self.ui_update.emit((alert_use_sample_data, ui))
                    
            except:
                def alert_no_sample_data_available(ui):
                    ui.label_17.setText(f"Server cannot be connected and no sample data available!")
                    loader = QtUiTools.QUiLoader()
                    ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                    ui_file.open(QtCore.QFile.ReadOnly)
                    dialog = loader.load(ui_file)
                    dialog.label.setText("Server cannot be connected")
                    dialog.label_2.setText("and no sample data available!")
                    dialog.exec_()
                self.ui_update.emit((alert_no_sample_data_available, ui))
                return
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
        return array_4d


class ReadDicomThread(QtCore.QThread):
    finished = QtCore.Signal(object)
    ui_update = QtCore.Signal(object)
    def __init__(self, filepath, ui):
        super().__init__()
        print("init ReadDicomThread")
        self._is_running = True
        self.filepath = filepath
        self.ui = ui

    def stop(self):
        self._is_running = False

    def run(self):
        print("run ReadDicomThread")
        serialized_data = self.read_dicom(self.filepath, self.ui)
        if self._is_running:
            self.finished.emit(serialized_data)

    def read_dicom(self, filepath, ui):
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
        
        NUM_FRAMES = image4D.shape[0]

        # ui progress bar
        def show_progress_bar(ui):
            ui.progressBar.setValue(10)
            ui.progressBar.setHidden(False)
        self.ui_update.emit((show_progress_bar, ui))
        # END

        # ui slider BEGIN
        def update_ui_slider(ui):
            ui.horizontalSlider.setMinimum(0)
            ui.horizontalSlider.setMaximum(NUM_FRAMES - 1)
            ui.label_12.setText("0")
            ui.label_13.setText(str(NUM_FRAMES - 1))
        self.ui_update.emit((update_ui_slider, ui))
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
        return serialized_data
    
def process_five_frames(frame, frame_index, five_frames, five_indexes):
    pickled_data = pickle.dumps(five_frames)
    compressed_data = blosc.compress(pickled_data)

    base_url = DataManager().server_base_url
    api = "process_five_frames_model_multiple" if DataManager().model_type == ModelType.MULTIPLE else "process_five_frames_model_unified"
    if not base_url.endswith("/"):
        base_url = base_url + "/"
    url = f"{base_url}{api}"
    headers = {"Content-Type": "application/octet-stream"}

    print(f"Request URL: {url}")

    try:
        response = requests.post(url, data=compressed_data, headers=headers)

        if response.status_code == 200:
            compressed_data = response.content

            # Decompress the received data
            pickled_data = blosc.decompress(compressed_data)

            # Deserialize the pickled data to a NumPy array
            view_to_array_2d: dict = pickle.loads(pickled_data)

            if api == "process_five_frames_model_unified":
                assert 'all' in view_to_array_2d.keys()
                new_view_to_array_2d = {}
                for view, indexes in PlaneReconstructionUtils.VIEW_STRUCTS.items():
                    if view == 'all':
                        continue
                    new_view_to_array_2d[view] = []
                    for ind in indexes:
                        new_view_to_array_2d[view].append(np.array(view_to_array_2d['all'][ind]))
                    new_view_to_array_2d[view] = np.array(new_view_to_array_2d[view])
                view_to_array_2d = new_view_to_array_2d

            print('Landmarks(Advanced): ')
            print(view_to_array_2d)
            with open(resource_path(os.path.join("pickle", f"{frame_index}.pickle")), "wb") as file:
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
    except Exception as e:
        print(e)
        print("Loading pickle data...")
        ## UI dialog is not needed since it's already displayed during the normalize_dicom_array API call
        try:
            with open(resource_path(os.path.join("pickle", f"{frame_index}.pickle")), "rb") as file:
                view_to_array_2d = pickle.load(file)
        except:
            ## TODO UI show error
            pass

    all_results = {}
    all_landmarks = {}
    i = 0
    for view, array_2d in view_to_array_2d.items():
        # print("---------------------------------------------------------------")
        # print(view)
        coords_raw = array_2d

        structures = PlaneReconstructionUtils.VIEW_STRUCTS[view]
        # print("Received: ", coords_raw)
        struct_counter=0
        for s in structures:
            all_landmarks[s] = coords_raw[struct_counter]
            struct_counter+=1

        st = time.perf_counter()
        # print(all_landmarks)
        try:

            # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
            # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
            # Note: You can modify time_index value to get plane visual from other time slices
            vs, coords_2d, coords_index, up_vector_2d, normal_3d, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y = PlaneReconstructionUtils.FindVisualFromCoordsOnce(
                    coords_raw, frame, view, truth=False, all_landmarks=all_landmarks)

            nx, ny, nz = normal_3d[0], normal_3d[1], normal_3d[2]
            rx, ry, rz = eulerFromNormal(nx, ny, nz)
            # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

            points = [coords_raw[i] for i in coords_index]
            center_point = find_center_point(points, DataManager().data_3d_padded_max_length)

            normalized_point = np.zeros(3)
            normalized_point[0] = center_point[0] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[1] = center_point[1] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[2] = center_point[2] / DataManager().data_3d_padded_max_length * 1.0

            cx, cy, cz = normalized_point
            # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

            # Rotate Image
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.HandleRotationsNumpy(vs, coords_2d, coords_index, up_vector_2d, view)
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.ViewSpecificRotations(slice_image, rotated_coords_2d, view)
            min_y = max_y = min_x = max_x = 0
            slice_image, rotated_coords_2d, min_y, max_y, min_x, max_x = PlaneReconstructionUtils.CropImageAndReturnPadding(slice_image, rotated_coords_2d, spacing=10)
            # Convert Image to PIL image
            slice_image = Image.fromarray(slice_image)
            slice_image = slice_image.convert("L")
            # pred_image.save(view + 'testing_pred.png')

            width, height = slice_image.size
            px = 1 / pyplot.rcParams['figure.dpi']
            pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
            pyplot.margins(x=0)
            pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
            pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
            pyplot.imshow(slice_image, cmap='gray')
            # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
            # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
            annotated_qimage = pyplot_to_qimage()

            et = time.perf_counter()
            # print("Execution time: ", et - st)

            all_results.update({view: (slice_image, rotated_coords_2d, annotated_qimage, rx, ry, rz, cx, cy, cz)})

        except Exception as e:
            print(e)
            all_results.update({view: None})

        i += 1
        view_to_array_2d[view] = [coords_2d, coords_raw, coords_index, up_vector_2d, normal_3d, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y, min_y, max_y, min_x, max_x]

    v0 = frame[106, :, :]
    v0 = np.rot90(v0, k=1) # rotate 270 degree clockwise
    v0 = Image.fromarray(v0)
    v0 = v0.convert("L")
    # v0.save("x=0.png") 
    v1 = frame[:, 106, :]
    v1 = np.rot90(v1, k=1) # rotate 270 degree clockwise
    v1 = Image.fromarray(v1)
    v1 = v1.convert("L")
    # v1.save("y=0.png")
    v2 = frame[:, :, 106]
    v2 = np.rot90(v2, k=1) # rotate 270 degree clockwise
    v2 = Image.fromarray(v2)
    v2 = v2.convert("L")
    # v2.save("z=0.png")

    all_center_images = {}
    all_center_images.update({"x=0": v0})
    all_center_images.update({"y=0": v1})
    all_center_images.update({"z=0": v2})
    return frame_index, all_results, view_to_array_2d, all_center_images

def process_frame(frame, frame_index):
    pickled_data = pickle.dumps(frame)
    compressed_data = blosc.compress(pickled_data)

    base_url = DataManager().server_base_url
    api = "process_frame_model_multiple" if DataManager().model_type == ModelType.MULTIPLE else "process_frame_model_unified"
    if not base_url.endswith("/"):
        base_url = base_url + "/"
    url = f"{base_url}{api}"
    headers = {"Content-Type": "application/octet-stream"}

    print(f"Request URL: {url}")

    try:
        response = requests.post(url, data=compressed_data, headers=headers)

        if response.status_code == 200:
            compressed_data = response.content

            # Decompress the received data
            pickled_data = blosc.decompress(compressed_data)

            # Deserialize the pickled data to a NumPy array
            view_to_array_2d: dict = pickle.loads(pickled_data)

            if api == "process_frame_model_unified":
                assert 'all' in view_to_array_2d.keys()
                new_view_to_array_2d = {}
                for view, indexes in PlaneReconstructionUtils.VIEW_STRUCTS.items():
                    if view == 'all':
                        continue
                    new_view_to_array_2d[view] = []
                    for ind in indexes:
                        new_view_to_array_2d[view].append(np.array(view_to_array_2d['all'][ind]))
                    new_view_to_array_2d[view] = np.array(new_view_to_array_2d[view])
                view_to_array_2d = new_view_to_array_2d

            print('Landmarks(Basic): ')
            print(view_to_array_2d)
            with open(resource_path(os.path.join("pickle", f"{frame_index}.pickle")), "wb") as file:
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
    except Exception as e:
        print(e)
        print("Loading pickle data...")
        ## UI dialog is not needed since it's already displayed during the normalize_dicom_array API call
        try:
            with open(resource_path(os.path.join("pickle", f"{frame_index}.pickle")), "rb") as file:
                view_to_array_2d = pickle.load(file)
        except:
            ## TODO UI show error
            pass

    all_results = {}
    all_landmarks = {}
    i = 0
    for view, array_2d in view_to_array_2d.items():
        # print("---------------------------------------------------------------")
        # print(view)
        coords_raw = array_2d

        structures = PlaneReconstructionUtils.VIEW_STRUCTS[view]
        # print("Received: ", coords_raw)
        struct_counter=0
        for s in structures:
            all_landmarks[s] = coords_raw[struct_counter]
            struct_counter+=1

        st = time.perf_counter()
        # print(all_landmarks)
        try:

            # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
            # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
            # Note: You can modify time_index value to get plane visual from other time slices
            vs, coords_2d, coords_index, up_vector_2d, normal_3d, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y = PlaneReconstructionUtils.FindVisualFromCoordsOnce(
                    coords_raw, frame, view, truth=False, all_landmarks=all_landmarks)

            nx, ny, nz = normal_3d[0], normal_3d[1], normal_3d[2]
            rx, ry, rz = eulerFromNormal(nx, ny, nz)
            # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

            points = [coords_raw[i] for i in coords_index]
            center_point = find_center_point(points, DataManager().data_3d_padded_max_length)

            normalized_point = np.zeros(3)
            normalized_point[0] = center_point[0] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[1] = center_point[1] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[2] = center_point[2] / DataManager().data_3d_padded_max_length * 1.0

            cx, cy, cz = normalized_point
            # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

            # Rotate Image
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.HandleRotationsNumpy(vs, coords_2d, coords_index, up_vector_2d, view)
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.ViewSpecificRotations(slice_image, rotated_coords_2d, view)
            min_y = max_y = min_x = max_x = 0
            slice_image, rotated_coords_2d, min_y, max_y, min_x, max_x = PlaneReconstructionUtils.CropImageAndReturnPadding(slice_image, rotated_coords_2d, spacing=10)
            # Convert Image to PIL image
            slice_image = Image.fromarray(slice_image)
            slice_image = slice_image.convert("L")
            # pred_image.save(view + 'testing_pred.png')

            width, height = slice_image.size
            px = 1 / pyplot.rcParams['figure.dpi']
            pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
            pyplot.margins(x=0)
            pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
            pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
            pyplot.imshow(slice_image, cmap='gray')
            # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
            # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
            annotated_qimage = pyplot_to_qimage()

            et = time.perf_counter()
            # print("Execution time: ", et - st)

            all_results.update({view: (slice_image, rotated_coords_2d, annotated_qimage, rx, ry, rz, cx, cy, cz)})

        except Exception as e:
            print(e)
            all_results.update({view: None})

        i += 1
        view_to_array_2d[view] = [coords_2d, coords_raw, coords_index, up_vector_2d, normal_3d, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y, min_y, max_y, min_x, max_x]

    v0 = frame[106, :, :]
    v0 = np.rot90(v0, k=1) # rotate 270 degree clockwise
    v0 = Image.fromarray(v0)
    v0 = v0.convert("L")
    # v0.save("x=0.png") 
    v1 = frame[:, 106, :]
    v1 = np.rot90(v1, k=1) # rotate 270 degree clockwise
    v1 = Image.fromarray(v1)
    v1 = v1.convert("L")
    # v1.save("y=0.png")
    v2 = frame[:, :, 106]
    v2 = np.rot90(v2, k=1) # rotate 270 degree clockwise
    v2 = Image.fromarray(v2)
    v2 = v2.convert("L")
    # v2.save("z=0.png")

    all_center_images = {}
    all_center_images.update({"x=0": v0})
    all_center_images.update({"y=0": v1})
    all_center_images.update({"z=0": v2})
    return frame_index, all_results, view_to_array_2d, all_center_images

def process_frame_with_known_matrix(frame, frame_index, view_to_array_2d):
    all_results = {}
    i = 0
    for view, info_list in view_to_array_2d.items():

        # isPerfectSlice means perfectly horizontal or vertical slice. so no calculations needed to extract.
        mapped_coords, coords_raw, mapped_coords_index, pred_up, normal, isPerfectSlice, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y, min_y, max_y, min_x, max_x = info_list

        st = time.perf_counter()

        try:
            # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
            # Note: You can modify time_index value to get plane visual from other time slices
            # pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, normal = PlaneReconstructionUtils.FindVisualFromCoords(
            #     pred_coords_raw, frame, view)
            visual = PlaneReconstructionUtils.FindVisualFromGivenInfo(
                    frame, isPerfectSlice, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y)

            nx, ny, nz = normal[0], normal[1], normal[2]
            rx, ry, rz = eulerFromNormal(nx, ny, nz)
            # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

            points = [coords_raw[i] for i in mapped_coords_index]
            center_point = find_center_point(points, DataManager().data_3d_padded_max_length)

            normalized_point = np.zeros(3)
            normalized_point[0] = center_point[0] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[1] = center_point[1] / DataManager().data_3d_padded_max_length * 1.0
            normalized_point[2] = center_point[2] / DataManager().data_3d_padded_max_length * 1.0

            cx, cy, cz = normalized_point
            # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")
            # Rotate Image
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.HandleRotationsNumpy(visual, mapped_coords, mapped_coords_index, pred_up, view)
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.ViewSpecificRotations(slice_image, rotated_coords_2d, view)
            slice_image, rotated_coords_2d = PlaneReconstructionUtils.CropImageWithGivenPadding(slice_image, rotated_coords_2d, min_y, max_y, min_x, max_x, spacing=10)
            
            # Convert Imag eto PIL image
            slice_image = Image.fromarray(slice_image)
            slice_image = slice_image.convert("L")
            # pred_image.save(view + 'testing_pred.png')

            width, height = slice_image.size
            px = 1 / pyplot.rcParams['figure.dpi']
            pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
            pyplot.margins(x=0)
            pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
            pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
            pyplot.imshow(slice_image, cmap='gray')
            # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
            # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
            annotated_qimage = pyplot_to_qimage()

            et = time.perf_counter()
            # print("Execution time: ", et - st)

            all_results.update({view: (slice_image, rotated_coords_2d, annotated_qimage, rx, ry, rz, cx, cy, cz)})

        except Exception as e:
            print(e)
            all_results.update({view: None})

        i += 1


    v0 = frame[106, :, :]
    v0 = np.rot90(v0, k=1) # rotate 270 degree clockwise
    v0 = Image.fromarray(v0)
    v0 = v0.convert("L")
    # v0.save("x=0.png") 
    v1 = frame[:, 106, :]
    v1 = np.rot90(v1, k=1) # rotate 270 degree clockwise
    v1 = Image.fromarray(v1)
    v1 = v1.convert("L")
    # v1.save("y=0.png")
    v2 = frame[:, :, 106]
    v2 = np.rot90(v2, k=1) # rotate 270 degree clockwise
    v2 = Image.fromarray(v2)
    v2 = v2.convert("L")
    # v2.save("z=0.png")

    all_center_images = {}
    all_center_images.update({"x=0": v0})
    all_center_images.update({"y=0": v1})
    all_center_images.update({"z=0": v2})
    return frame_index, all_results, all_center_images

# def process_frame_with_known_landmarks(frame, frame_index, view_to_array_2d):
#     all_results = {}
#     i = 0
#     for view, array_2d in view_to_array_2d.items():
#         pred_coords_raw = array_2d

#         st = time.perf_counter()

#         try:
#             # extract the content of the plane and project onto 2d image. Also do the same for the coordinates for visualization.
#             # pred_vs, pred_mapped_coords, pred_up = FindVisualFromCoords(pred_coords_raw, data_3d_padded)
#             # Note: You can modify time_index value to get plane visual from other time slices
#             pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, normal = PlaneReconstructionUtils.FindVisualFromCoords(
#                 pred_coords_raw, frame, view)
            
#             # pred_mapped_coords, pred_mapped_coords_index, pred_up, normal, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y = PlaneReconstructionUtils.FindVisualFromCoordsOnce(
#             #         pred_coords_raw, frame, view)

#             nx, ny, nz = normal[0], normal[1], normal[2]
#             rx, ry, rz = eulerFromNormal(nx, ny, nz)
#             # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")

#             points = [pred_coords_raw[i] for i in pred_mapped_coords_index]
#             center_point = find_center_point(points)

#             normalized_point = np.zeros(3)
#             normalized_point[0] = center_point[0] / 213.0
#             normalized_point[1] = center_point[1] / 213.0
#             normalized_point[2] = center_point[2] / 213.0

#             cx, cy, cz = normalized_point
#             # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

#             # Rotate Image
#             pred_image, pred_rotated_coords = PlaneReconstructionUtils.HandleRotationsNumpy(pred_vs, pred_mapped_coords, pred_mapped_coords_index, pred_up, view)
   
#             pred_image, pred_rotated_coords = PlaneReconstructionUtils.ViewSpecificRotations(pred_image, pred_rotated_coords, view)
            
#             # Convert Imag eto PIL image
#             pred_image = Image.fromarray(pred_image)
#             pred_image = pred_image.convert("L")
#             # pred_image.save(view + 'testing_pred.png')

#             width, height = pred_image.size
#             px = 1 / pyplot.rcParams['figure.dpi']
#             pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
#             pyplot.margins(x=0)
#             pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
#             pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())
#             pyplot.imshow(pred_image, cmap='gray')
#             # pyplot.scatter(pred_rotated_coords[:,0], pred_rotated_coords[:,1], c='red', marker='x')
#             # pyplot.savefig(str(frame_index * len(view_to_array_2d) + i) + '.png', bbox_inches='tight', pad_inches=0)
#             annotated_qimage = pyplot_to_qimage()

#             et = time.perf_counter()
#             print("Execution time: ", et - st)  # 7.5s on jerry's computer

#             all_results.update({view: (pred_image, pred_rotated_coords, annotated_qimage, rx, ry, rz, cx, cy, cz)})

#         except Exception as e:
#             print(e)
#             all_results.update({view: None})

#         i += 1


#     return frame_index, all_results

def thread_pool_test(frame, frame_index):
    r = random.randint(5, 7)
    time.sleep(r)
    print("Worker thread finishing")
    return (frame_index, r)

def pyplot_to_qimage():
    buf = io.BytesIO()
    pyplot.savefig(buf, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return QtGui.QImage.fromData(buf.getvalue())