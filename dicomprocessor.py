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
from euler import eulerFromNormal, find_center_point


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
        print("---------------------------------------------------------------")
        print(view)
        coords_raw = array_2d

        structures = PlaneReconstructionUtils.VIEW_STRUCTS[view]
        print("Received: ", coords_raw)
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

def process_dicom(analyze_all, array_4d, ui: Ui_MainWindow, selected_frame_index):
    data_4d_padded = array_4d

    # print(data_4d_padded)
    print(data_4d_padded.shape)

    DataManager().data_3d_padded_max_length = data_4d_padded.shape[1]

    NUM_FRAMES = data_4d_padded.shape[0]
    print(f"NUM_FRAMES: {NUM_FRAMES}")

    if (selected_frame_index == -1):
        selected_frame_index = int(NUM_FRAMES / 2)

    DataManager().clear_all_results()
    ui.gridWidget.clearAllItems(ui.gridWidget)

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

        frame_index, all_results, view_to_array_2d, all_center_images = result.get()

        DataManager().update_pred_result(frame_index, all_results)
        DataManager().update_center_images(frame_index, all_center_images)

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
                process_frame_with_known_matrix,
                # process_frame_with_known_landmarks,
                args=(
                    data_3d_padded,
                    i,
                    view_to_array_2d,
                ),
            )

            frame_index, all_results, all_center_images = result.get()

            DataManager().update_pred_result(frame_index, all_results)
            DataManager().update_center_images(frame_index, all_center_images)
    
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

def pyplot_to_qimage():
    buf = io.BytesIO()
    pyplot.savefig(buf, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return QtGui.QImage.fromData(buf.getvalue())