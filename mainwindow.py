import sys
from util import resource_path
from PySide2 import QtGui, QtUiTools, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QAction, QMenu, QInputDialog, QComboBox, QWidgetAction
from ui_mainwindow import Ui_MainWindow
import os
import threading
import pickle
import blosc
import base64
import requests
import cv2
import numpy as np
from formatconverter import dicom_to_array, pad4d
from dicomprocessor import process_dicom
from datamanager import DataManager, ModelType
from clickableqlabel import ClickableQLabel
from model import Quad, Line


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_22.setText(DataManager().VERSION)

        ## private UI data
        self._current_frame_index = 0
        ##

        #### Top Menu Bar BEGIN ####
        self.action_import_all_time_frame = QAction("Analyze all time frames", self)
        self.action_import_all_time_frame.triggered.connect(self.import_dicom_and_analyze_all)

        self.action_import_selected_time_frame = QAction("Analyze only the selected time frame", self)
        self.action_import_selected_time_frame.triggered.connect(self.import_dicom_and_analyze_selected)

        ### Export all cross-section images in all time frames
        self.action_export_all_cross_section_all_time_frames = QAction("Export videos of all views", self)
        self.action_export_all_cross_section_all_time_frames.triggered.connect(self.export_all)
        
        ### Export all cross-section images in the current time frame
        self.action_export_all_cross_section_selected_time_frame = QAction("Export images of all views in the current time frame", self)
        self.action_export_all_cross_section_selected_time_frame.triggered.connect(self.export_selected_time_frame)

        # Create a Set Server Address action
        self.action_set_server = QAction("Set Server Base URL (e.g. http://localhost:8000/)", self)
        self.action_set_server.triggered.connect(self.set_server_address)

        # Create menus
        self.import_menu = QMenu("Import and Process DICOM file", self)
        self.import_menu.addAction(self.action_import_all_time_frame)
        self.import_menu.addAction(self.action_import_selected_time_frame)

        self.export_menu = QMenu("Export cross-section images", self)
        self.export_menu.addAction(self.action_export_all_cross_section_all_time_frames)
        self.export_menu.addAction(self.action_export_all_cross_section_selected_time_frame)

        self.options_menu = QMenu("Options", self)
        self.options_menu.addAction(self.action_set_server)

        #### Select model
        # Create the combo box
        self.select_model_combo_box = QComboBox()
        self.select_model_combo_box.addItem(ModelType.MULTIPLE.value)
        self.select_model_combo_box.addItem(ModelType.UNIFIED.value)
        self.select_model_combo_box.setCurrentText(DataManager().model_type.value)
        self.select_model_combo_box.activated.connect(self.on_select_model)

        # Create the action for the submenu
        self.select_model_sub_menu_action = QWidgetAction(self)

        # Set the combo box as the default widget for the action
        self.select_model_sub_menu_action.setDefaultWidget(self.select_model_combo_box)
        self.select_model_submenu = self.options_menu.addMenu("Select machine learning model")
        self.select_model_submenu.addAction(self.select_model_sub_menu_action)
        #### Select model END

        # Create menu bar
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(self.import_menu)
        self.menu_bar.addMenu(self.export_menu)
        self.menu_bar.addMenu(self.options_menu)
        # Set menu bar as the main window's menu bar
        self.setMenuBar(self.menu_bar)

        # print(self.import_menu.styleSheet())
        # print(self.menu_bar.styleSheet())
        ## Style sheet BEGIN ##
        menuBarStylesheet = """
QMenuBar {
    font: 15px "MS Shell Dlg 2";
    background-color: #f2f2f2;
    padding: 5px 5px;
}
"""
        self.menu_bar.setStyleSheet(menuBarStylesheet)

        importMenuStylesheet = """ 
QMenu {
    font: 15px "MS Shell Dlg 2";
    background-color: #f2f2f2;
}

QMenu::item {
    font: 15px "MS Shell Dlg 2";
    padding: 5px 20px;
}

QMenu::item:selected {
    font: 15px "MS Shell Dlg 2";
    background-color: #007BFF;
    color: #ffffff;
}
"""
        # self.import_menu.setStyleSheet(importMenuStylesheet)
        ## Style sheet END ##
        #### Top Menu Bar END ####
        
        self.ui.progressBar.setHidden(True)

        self.ui.horizontalSlider.valueChanged.connect(self.frame_index_changed)
        self.ui.pushButton_21.clicked.connect(lambda: self.play_or_pause_cross_section(self.ui.pushButton_21))
        self.clearAllCrossSections()

    def on_select_model(self, index):
        combo_box = self.sender()
        selected_option = combo_box.itemText(index)
        print(f"Selected Option: {selected_option} combobox[{index}] enum[{ModelType(selected_option).name}]")
        DataManager().model_type = ModelType(selected_option)

    def set_server_address(self):
        address, ok = QInputDialog.getText(self, "Server Address", "Enter the server address:", text=DataManager().server_base_url)

        if ok:
            # Do something with the server address (e.g., store it, use it for connection, etc.)
            print("Server address:", address)
            DataManager().server_base_url = address
            try:
                response = requests.get(address)
                loader = QtUiTools.QUiLoader()
                ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                ui_file.open(QtCore.QFile.ReadOnly)
                dialog = loader.load(ui_file)
                dialog.setWindowTitle("Notification")
                dialog.label.setText("Server connection test successful!")
                dialog.label_2.setText("")
                dialog.exec_()
            except:
                loader = QtUiTools.QUiLoader()
                ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                ui_file.open(QtCore.QFile.ReadOnly)
                dialog = loader.load(ui_file)
                dialog.label.setText("Server cannot be connected!")
                dialog.label_2.setText("")
                dialog.exec_()
        
    def export_all(self):
        dialog = QFileDialog()        
        folder_path = dialog.getExistingDirectory(self, "Select folder to save PNG files")
       
        if folder_path == "":
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid folder!")
            dialog.label_2.setText("")
            dialog.exec_()
            return
        
        NUM_FRAMES = DataManager().dicom_number_of_frames
        if NUM_FRAMES == -1 or NUM_FRAMES == 0:
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("No result to save yet!")
            dialog.label_2.setText("")
            dialog.exec_()
            return
        try:
            ## Save as video
            view_to_video_writer = {}
            if not NUM_FRAMES == 0:
                all_results = DataManager().get_pred_result(0)
                if not all_results == None:
                    for view, pred_result in all_results.items():
                        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result
                        width = annotated_qimage.width()
                        height = annotated_qimage.height()
                        output_file = os.path.join(folder_path, f"{view}.mp4")
                        frame_rate = int(DataManager().dicom_fps)
                        view_to_video_writer[view] = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (width, height))
            ## Save as video END
            for frame_index in range(NUM_FRAMES):
                all_results = DataManager().get_pred_result(frame_index)

                if all_results == None:
                    loader = QtUiTools.QUiLoader()
                    ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                    ui_file.open(QtCore.QFile.ReadOnly)
                    dialog = loader.load(ui_file)
                    dialog.setWindowTitle("Notification")
                    dialog.label.setText("Some results are not ready!")
                    dialog.label_2.setText("The ready results have been saved.")
                    dialog.exec_()
                    raise Exception("Some results are not ready!")
                else:
                    for view, pred_result in all_results.items():
                        if pred_result is None:
                            loader = QtUiTools.QUiLoader()
                            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                            ui_file.open(QtCore.QFile.ReadOnly)
                            dialog = loader.load(ui_file)
                            dialog.label.setText("Some result is broken!")
                            dialog.label_2.setText("Not all results are saved!")
                            dialog.exec_()
                            raise Exception("Some pred_result is None!")
                        else:
                            _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

                            #### Comment out the save all images part
                            # filename = f"frame-{frame_index}-view-{view}.png"

                            # frame_index_dir = os.path.join(folder_path, str(frame_index))
                            # if not os.path.exists(frame_index_dir):
                            #     os.mkdir(frame_index_dir)
                            # annotated_qimage.save(f"{os.path.join(frame_index_dir, filename)}")
                            #### Comment out the save all images part END

                            ## Save as video
                            # Convert QImage to numpy array
                            width = annotated_qimage.width()
                            height = annotated_qimage.height()
                            annotated_qimage = annotated_qimage.convertToFormat(QtGui.QImage.Format_RGB32)
                            ptr = annotated_qimage.constBits()
                            numpy_frame = np.array(ptr).reshape(height, width, 4)  #  Copies the data
                            numpy_frame = numpy_frame[:, :, :3]

                            # Convert BGR to RGB
                            numpy_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2RGB)

                            # Write the frame to the video writer
                            view_to_video_writer[view].write(numpy_frame)
                            ## Save as video END
            
            ## Save as video
            for view, video_writer in view_to_video_writer.items():
                video_writer.release()
            ## Save as video END

            print("All files saved successfully.")
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.setWindowTitle("Notification")
            dialog.label.setText("All files saved successfully.")
            dialog.label_2.setText("")
            dialog.exec_()
        except Exception as e:
            print(e)

    def export_selected_time_frame(self):
        frame_index = self._current_frame_index

        dialog = QFileDialog()        
        folder_path = dialog.getExistingDirectory(self, "Select folder to save PNG files")
       
        if folder_path == "":
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid folder!")
            dialog.label_2.setText("")
            dialog.exec_()
            return 
        try:
            all_results = DataManager().get_pred_result(frame_index)

            if all_results == None:
                loader = QtUiTools.QUiLoader()
                ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                ui_file.open(QtCore.QFile.ReadOnly)
                dialog = loader.load(ui_file)
                dialog.label.setText("No result to save yet!")
                dialog.label_2.setText("")
                dialog.exec_()
                raise Exception("No result to save yet!")
            else:
                for view, pred_result in all_results.items():
                    if pred_result is None:
                        loader = QtUiTools.QUiLoader()
                        ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                        ui_file.open(QtCore.QFile.ReadOnly)
                        dialog = loader.load(ui_file)
                        dialog.label.setText("Some result is broken!")
                        dialog.label_2.setText("Not all results are saved!")
                        dialog.exec_()
                        raise Exception("Some pred_result is None!")
                    else:
                        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

                        filename = f"frame-{frame_index}-view-{view}.png"
                        annotated_qimage.save(f"{os.path.join(folder_path, filename)}")
                
            print("All files saved successfully.")
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.setWindowTitle("Notification")
            dialog.label.setText("All files saved successfully.")
            dialog.label_2.setText("")
            dialog.exec_()
        except Exception as e:
            print(e)

    def play_or_pause_cross_section(self, button):
        if self.is_playing(button) == None:
            print(f"Play/Pause button {button} is broken!")
            return
        elif self.is_playing(button) == False:
            old_style_sheet = self.ui.pushButton_21.styleSheet()
            new_style_sheet = old_style_sheet.replace(":/images/icons8-play-button-48.png", ":/images/icons8-pause-button-48.png")
            self.ui.pushButton_21.setStyleSheet(new_style_sheet)

            current = self.ui.horizontalSlider.value()
            if current == self.ui.horizontalSlider.maximum():
                self.ui.horizontalSlider.setValue(0)

            self.play_timer = QtCore.QTimer()
            self.play_timer.timeout.connect(self.increment_frame_index)
            self.play_delta_time = DataManager().dicom_average_frame_time_in_ms
            self.play_timer.start(self.play_delta_time)
        else:
            old_style_sheet = self.ui.pushButton_21.styleSheet()
            new_style_sheet = old_style_sheet.replace(":/images/icons8-pause-button-48.png", ":/images/icons8-play-button-48.png")
            self.ui.pushButton_21.setStyleSheet(new_style_sheet)

            self.play_timer.stop()

    def is_playing(self, button):
        if ":/images/icons8-play-button-48.png" in button.styleSheet():
            return False
        elif ":/images/icons8-pause-button-48.png" in button.styleSheet():
            return True
        return None

    def increment_frame_index(self):
        current = self.ui.horizontalSlider.value()
        if current == self.ui.horizontalSlider.maximum():
            old_style_sheet = self.ui.pushButton_21.styleSheet()
            new_style_sheet = old_style_sheet.replace(":/images/icons8-pause-button-48.png", ":/images/icons8-play-button-48.png")
            self.ui.pushButton_21.setStyleSheet(new_style_sheet)

            self.play_timer.stop()
        else:
            self.ui.horizontalSlider.setValue(current + 1)

    def frame_index_changed(self, slider_value):
        # print(slider_value)

        frame_index: int = slider_value
        self._current_frame_index = frame_index

        self.ui.label_10.setText(f"Selected time frame index: {frame_index}")

        all_results = DataManager().get_pred_result(frame_index)
        all_center_images = DataManager().get_center_images(frame_index)
        
        if all_results == None:
            self.clearAllCrossSections()
        else:
            ## Update OpenGL cross sections
            app = self.ui.openGLWidget
            app.scene.objects.clear()
            add = app.scene.add_object
            add(Quad(app, tex_pil=all_center_images.get("x=0"), pos=(0, 0, 0), rot=(0, -90, 0), brightness=1.0)) # x=0
            add(Quad(app, tex_pil=all_center_images.get("y=0"), pos=(0, 0, 0), rot=(0, 0, 0), brightness=1.0)) # y=0
            add(Quad(app, tex_pil=all_center_images.get("z=0"), pos=(0, 0, 0), rot=(90, 0, 0), brightness=1.0)) # z=0
            add(Line(app, pos=(1, 0, 0), color=(1, 0, 0, 1))) # x-axis
            add(Line(app, pos=(0, 1, 0), rot=(0, 0, 90), color=(0, 1, 0, 1))) # y-axis
            add(Line(app, pos=(0, 0, 1), rot=(0, 90, 0), color=(0, 0, 1, 1))) # z-axis
            add(Line(app, pos=(0, -1, -1)))
            add(Line(app, pos=(0, -1, 1)))
            add(Line(app, pos=(0, 1, -1)))
            add(Line(app, pos=(0, 1, 1)))
            add(Line(app, pos=(-1, -1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(-1, 1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(1, -1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(1, 1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(-1, 0, -1), rot=(0, 0, 90)))
            add(Line(app, pos=(-1, 0, 1), rot=(0, 0, 90)))
            add(Line(app, pos=(1, 0, -1), rot=(0, 0, 90)))
            add(Line(app, pos=(1, 0, 1), rot=(0, 0, 90)))
            ####

            if self.shouldInit():
                initAll = True
            else:
                initAll = False
            for view, pred_result in all_results.items():
                if pred_result == None:
                    print(f"At frame index {frame_index}, the pred_result for view {view} is None!")
                    # first_found_width = DataManager().get_result_width(view)
                    # if not first_found_width == None:
                    # Add placeholder cross section
                    self.addPlaceholderCrossSection(view)
                    print(f"Placeholder cross section for view {view} has been added.")
                else:
                    try:
                        # pred_image, pred_rotated_coords, annotated_qimage = pred_result
                        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

                        # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")
                        # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

                        gl_cx = cx * 2.0 - 1.0
                        gl_cy = cz * 2.0 - 1.0
                        gl_cz = -1 * (cy * 2.0 - 1.0)

                        # print(f"view: {view}; (gl_cx, gl_cy, gl_cz): ({gl_cx}, {gl_cy}, {gl_cz})")

                        brightness = 1.0
                        highlighted_view = DataManager().highlighted_view
                        if highlighted_view == view:
                            print(f"Highlighted view: {view}")
                            brightness = 45.0
                        # else:
                            # print("Highlighted view does not match with the current")

                        ## Update OpenGL cross sections
                        crossSection3D = Quad(app, tex_id="skybox", pos=(gl_cx, gl_cy, gl_cz), rot=(rx - 90, ry, rz), brightness=brightness)
                        add(crossSection3D)
                        ####
                        
                        DataManager().update_result_width(view, annotated_qimage.width())

                        if initAll:
                            self.addCrossSection(annotated_qimage, view, frame_index)
                        else:
                            self.modifyCrossSection(annotated_qimage, view, frame_index)
                    except Exception as e:
                        print(e)

    def import_dicom_and_analyze_all(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File, in which all time frames will be analyzed"),
            os.getcwd(),
            self.tr("DICOM File (*.dcm)"),
        )
        filepath = file[0]
        
        if filepath == "": # No file is selected
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid filepath!")
            dialog.label_2.setText("")
            dialog.exec_()
            return
        
        event = threading.Event()
        t1 = threading.Thread(
            target=self.read_dicom,
            args=(
                filepath,
                self.ui,
                event,
            ),
        )
        t1.start()

        # Create a QTimer
        self.read_dicom_timer = QtCore.QTimer()
        self.read_dicom_timer.timeout.connect(lambda: self.check_completion_analyze_all(event))
        self.read_dicom_timer.start(16)

    def check_completion_analyze_all(self, event):
        if not event.is_set():
            # Perform any non-blocking UI updates or other tasks
            # print("UI update or other task while waiting...")
            pass
        else:
            self.read_dicom_timer.stop()

            serialized_data = event.result

            array_4d = self.send_dicom(serialized_data, self.ui)

            t2 = threading.Thread(
                target=process_dicom,
                args=(
                    True,
                    array_4d,
                    self.ui,
                    -1,
                ),
            )
            t2.start()

    def import_dicom_and_analyze_selected(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File, in which only the selected time frame will be analyzed"),
            os.getcwd(),
            self.tr("DICOM File (*.dcm)"),
        )
        filepath = file[0]

        if filepath == "": # No file is selected
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid filepath!")
            dialog.label_2.setText("")
            dialog.exec_()
            return

        event = threading.Event()
        t1 = threading.Thread(
            target=self.read_dicom,
            args=(
                filepath,
                self.ui,
                event,
            ),
        )
        t1.start()

        # Create a QTimer
        self.read_dicom_timer = QtCore.QTimer()
        self.read_dicom_timer.timeout.connect(lambda: self.check_completion_analyze_selected(event))
        self.read_dicom_timer.start(16)

    def check_completion_analyze_selected(self, event):
        if not event.is_set():
            # Perform any non-blocking UI updates or other tasks
            # print("UI update or other task while waiting...")
            pass
        else:
            self.read_dicom_timer.stop()

            serialized_data = event.result

            array_4d = self.send_dicom(serialized_data, self.ui)

            t2 = threading.Thread(
                target=process_dicom,
                args=(
                    False,
                    array_4d,
                    self.ui,
                    # self.ui.horizontalSlider.value(),
                    -1,
                ),
            )
            t2.start()

    def read_dicom(self, filepath, ui, event):
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
        
        self.display_video_info(ui)

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
        event.result = serialized_data
        event.set()

    def send_dicom(self, serialized_data, ui):
        base_url = DataManager().server_base_url
        if not base_url.endswith("/"):
            base_url = base_url + "/"
        url = f"{base_url}normalize_dicom_array"
        headers = {"Content-Type": "application/octet-stream"}
        try:
            response = requests.post(url, data=serialized_data, headers=headers)

            ui.label_17.setText(f"DICOM File (Video) Info:")

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
                loader = QtUiTools.QUiLoader()
                ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                ui_file.open(QtCore.QFile.ReadOnly)
                dialog = loader.load(ui_file)
                dialog.label.setText("normalize_dicom_array response is not 200")
                dialog.label_2.setText("")
                dialog.exec_()
                return
        except:
            try:
                with open(resource_path(os.path.join("pickle", "array_4d.pickle")), "rb") as file:
                    array_4d = pickle.load(file)
                    print("Loading pickle data...")
                    loader = QtUiTools.QUiLoader()
                    ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                    ui_file.open(QtCore.QFile.ReadOnly)
                    dialog = loader.load(ui_file)
                    dialog.setWindowTitle("Notification")
                    dialog.label.setText("Server cannot be connected!")
                    dialog.label_2.setText("Loading sample data...")
                    dialog.exec_()
                    ui.label_17.setText(f"(Using Sample Data) DICOM File (Video) Info:")
            except:
                ui.label_17.setText(f"Server cannot be connected and no sample data available!")
                loader = QtUiTools.QUiLoader()
                ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                ui_file.open(QtCore.QFile.ReadOnly)
                dialog = loader.load(ui_file)
                dialog.label.setText("Server cannot be connected")
                dialog.label_2.setText("and no sample data available!")
                dialog.exec_()
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
    
    def display_video_info(self, ui: Ui_MainWindow):
        ui.label_16.setText(f"Video - Number of Frames: {DataManager().dicom_number_of_frames}")
        ui.label_15.setText(f"Video - Average Frame Time: {round(DataManager().dicom_average_frame_time_in_ms, 2)}ms")
        ui.label_9.setText(f"Video - FPS: {round(DataManager().dicom_fps, 2)}")
        ui.label_14.setText(f"Video - Total Duration: {round(DataManager().dicom_total_duration_in_s, 2)}s")

    def setHighlight(self, view, frame_index):
        if DataManager().highlighted_view == view:
            DataManager().highlighted_view = ""
        else:
            DataManager().highlighted_view = view
        all_results = DataManager().get_pred_result(frame_index)
        all_center_images = DataManager().get_center_images(frame_index)
        if not all_results == None:
            ## Update OpenGL cross sections
            app = self.ui.openGLWidget
            app.scene.objects.clear()
            add = app.scene.add_object
            add(Quad(app, tex_pil=all_center_images.get("x=0"), pos=(0, 0, 0), rot=(0, -90, 0), brightness=1.0)) # x=0
            add(Quad(app, tex_pil=all_center_images.get("y=0"), pos=(0, 0, 0), rot=(0, 0, 0), brightness=1.0)) # y=0
            add(Quad(app, tex_pil=all_center_images.get("z=0"), pos=(0, 0, 0), rot=(90, 0, 0), brightness=1.0)) # z=0
            add(Line(app, pos=(1, 0, 0), color=(1, 0, 0, 1))) # x-axis
            add(Line(app, pos=(0, 1, 0), rot=(0, 0, 90), color=(0, 1, 0, 1))) # y-axis
            add(Line(app, pos=(0, 0, 1), rot=(0, 90, 0), color=(0, 0, 1, 1))) # z-axis
            add(Line(app, pos=(0, -1, -1)))
            add(Line(app, pos=(0, -1, 1)))
            add(Line(app, pos=(0, 1, -1)))
            add(Line(app, pos=(0, 1, 1)))
            add(Line(app, pos=(-1, -1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(-1, 1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(1, -1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(1, 1, 0), rot=(0, 90, 0)))
            add(Line(app, pos=(-1, 0, -1), rot=(0, 0, 90)))
            add(Line(app, pos=(-1, 0, 1), rot=(0, 0, 90)))
            add(Line(app, pos=(1, 0, -1), rot=(0, 0, 90)))
            add(Line(app, pos=(1, 0, 1), rot=(0, 0, 90)))
            ####

            for view, pred_result in all_results.items():
                if pred_result == None:
                    print(f"At frame index {frame_index}, the pred_result for view {view} is None!")
                else:
                    try:
                        # pred_image, pred_rotated_coords, annotated_qimage = pred_result
                        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

                        # print(f"view: {view}; (rx, ry, rz): ({rx}, {ry}, {rz})")
                        # print(f"view: {view}; (cx, cy, cz): ({cx}, {cy}, {cz})")

                        gl_cx = cx * 2.0 - 1.0
                        gl_cy = cz * 2.0 - 1.0
                        gl_cz = -1 * (cy * 2.0 - 1.0)

                        # print(f"view: {view}; (gl_cx, gl_cy, gl_cz): ({gl_cx}, {gl_cy}, {gl_cz})")

                        brightness = 1.0
                        highlighted_view = DataManager().highlighted_view
                        if highlighted_view == view:
                            print(f"Highlighted view: {view}")
                            brightness = 45.0
                        # else:
                        #     print("Highlighted view does not match with the current")

                        ## Update OpenGL cross sections
                        crossSection3D = Quad(app, tex_id="skybox", pos=(gl_cx, gl_cy, gl_cz), rot=(rx - 90, ry, rz), brightness=brightness)
                        add(crossSection3D)
                        ####
                        
                    except Exception as e:
                        print(e)

    def export(self, annotated_qimage, view, frame_index):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".png")
        default_filename = f"frame-{frame_index}-view-{view}"
        file_path, _ = dialog.getSaveFileName(self, "Save PNG", default_filename, "PNG Files (*.png)")

        if file_path:
            annotated_qimage.save(f"{file_path}.png")
            print("File saved successfully.")

    def counterclockwiseRotate90(self, annotated_qimage, label, view, frame_index):
        print(f"counterclockwiseRotate({annotated_qimage}, {label}, {label.tag}, {view}, {frame_index})")
        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        new_degree = (int(label.tag.split(",")[2]) - 90) % 360

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N
        
        transform = QtGui.QTransform().rotate(new_degree)
        pixmap = pixmap.transformed(transform)
        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label.setPixmap(pixmap)
        label.tag = f"{view},{frame_index},{new_degree}"
        label.show()

    def clockwiseRotate90(self, annotated_qimage, label, view, frame_index):
        print(f"clockwiseRotate({annotated_qimage}, {label}, {label.tag}, {view}, {frame_index})")
        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        new_degree = (int(label.tag.split(",")[2]) + 90) % 360

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N
        
        transform = QtGui.QTransform().rotate(new_degree)
        pixmap = pixmap.transformed(transform)
        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label.setPixmap(pixmap)
        label.tag = f"{view},{frame_index},{new_degree}"
        label.show()

    def findCrossSection(self, grid_layout, view):
        i = 0
        for row in range(grid_layout.rowCount()):
            for column in range(grid_layout.columnCount()):
                child = grid_layout.itemAtPosition(row, column).widget()
                tag = child.findChild(QLabel, "label_8").tag
                if tag.split(",")[0] == view:
                    cross_section = child
                    return cross_section
                i = i + 1
                if i == grid_layout.count():
                    return None
        return None

    def modifyCrossSection(self, annotated_qimage, view, frame_index):
        grid_layout = self.ui.gridWidget.layout()
        cross_section = self.findCrossSection(grid_layout, view)

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N

        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label = cross_section.findChild(QLabel, "label_8")
        label.setPixmap(pixmap)

        # if label.tag == "":
        #     label.tag = f"{view},{frame_index},0"
        # else:
        #     # TODO more serious error handling
        #     new_degree = (int(label.tag.split(",")[2]) - 90) % 360
        #     label.tag = f"{view},{frame_index},{new_degree}"
        label.tag = f"{view},{frame_index},0"

        label.show()

        # view_button = cross_section.findChild(QPushButton, "pushButton_13")
        # view_button.setText(view)
        # view_button.clicked.connect(lambda: self.setHighlight(view, frame_index))

        # export_button = cross_section.findChild(QPushButton, "pushButton_9")
        # export_button.clicked.connect(lambda: self.export(annotated_qimage, view, frame_index))

        # counterclockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton")
        # clockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton_2")
        # counterclockwise_rotate_button.clicked.connect(lambda: self.counterclockwiseRotate90(annotated_qimage, label, view, frame_index))
        # clockwise_rotate_button.clicked.connect(lambda: self.clockwiseRotate90(annotated_qimage, label, view, frame_index))

        # self.ui.gridWidget.addWidget(cross_section)
        fixed_width = new_pixmap_width
        label.parent().setFixedWidth(fixed_width)
        label.setFixedHeight(fixed_width)

    def shouldInit(self):
        count = self.ui.gridWidget.layout().count()
        if count == 0:
            return True
        return False

    def addCrossSection(self, annotated_qimage, view, frame_index):
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(ClickableQLabel)
        ui_file = QtCore.QFile(resource_path("crosssection.ui"))
        ui_file.open(QtCore.QFile.ReadOnly)
        cross_section = loader.load(ui_file)
        ui_file.close()

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N

        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label = cross_section.findChild(QLabel, "label_8")
        label.setPixmap(pixmap)

        # if label.tag == "":
        #     label.tag = f"{view},{frame_index},0"
        # else:
        #     # TODO more serious error handling
        #     new_degree = (int(label.tag.split(",")[2]) - 90) % 360
        #     label.tag = f"{view},{frame_index},{new_degree}"
        label.tag = f"{view},{frame_index},0"

        label.show()

        view_button = cross_section.findChild(QPushButton, "pushButton_13")
        view_button.setText(view)
        view_button.clicked.connect(lambda: self.setHighlight(view, frame_index))

        export_button = cross_section.findChild(QPushButton, "pushButton_9")
        export_button.clicked.connect(lambda: self.export(annotated_qimage, view, frame_index))

        counterclockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton")
        clockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton_2")
        counterclockwise_rotate_button.clicked.connect(lambda: self.counterclockwiseRotate90(annotated_qimage, label, view, frame_index))
        clockwise_rotate_button.clicked.connect(lambda: self.clockwiseRotate90(annotated_qimage, label, view, frame_index))

        self.ui.gridWidget.addWidget(cross_section)
        fixed_width = new_pixmap_width
        label.parent().setFixedWidth(fixed_width)
        label.setFixedHeight(fixed_width)

    def addPlaceholderCrossSection(self, view):
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(ClickableQLabel)
        ui_file = QtCore.QFile(resource_path("crosssection.ui"))
        ui_file.open(QtCore.QFile.ReadOnly)
        cross_section = loader.load(ui_file)
        ui_file.close()

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N

        pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(new_pixmap_width, 0, QtGui.QImage.Format_RGB888))
        label = cross_section.findChild(QLabel, "label_8")
        label.setPixmap(pixmap)
        label.show()

        view_button = cross_section.findChild(QPushButton, "pushButton_13")
        view_button.setText(view)

        self.ui.gridWidget.addWidget(cross_section)

    def clearAllCrossSections(self):
        self.ui.gridWidget.clearAllItems(self.ui.gridWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
