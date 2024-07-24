import sys
from util import resource_path
from PySide2 import QtGui, QtUiTools, QtCore, QtWidgets
# from PySide2.QtGui import QIcon
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
from dicomprocessor import ReadDicomThread, SendDicomThread, ProcessDicomThread
from datamanager import DataManager, ModelType
from clickableqlabel import ClickableQLabel
from patienteditor import PatientEditor
from model import Quad, Line


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_22.setText(DataManager().VERSION)

        ## private UI data
        self._current_frame_index = 0
        self._is_first_patient = True
        self.read_dicom_thread = None
        self.send_dicom_thread = None
        self.process_dicom_thread = None
        ##

        #### Top Menu Bar BEGIN ####
        # self.action_import_five_time_frames = QAction("Analyze five time frames", self)
        # self.action_import_five_time_frames.triggered.connect(self.import_dicom_and_analyze_five_frames)

        self.action_import_selected_time_frame = QAction("Apical View", self)
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
        # self.import_menu.addAction(self.action_import_five_time_frames)
        self.import_menu.addAction(self.action_import_selected_time_frame)

        self.export_menu = QMenu("Export cross-section images", self)
        self.export_menu.addAction(self.action_export_all_cross_section_all_time_frames)
        self.export_menu.addAction(self.action_export_all_cross_section_selected_time_frame)

        self.options_menu = QMenu("Options", self)

        # Enable LVEF & LAV
        self.toggle_action = QAction("Toggle LVEF & LAV predictions", self)
        self.toggle_action.triggered.connect(self.toggle_layout_visibility)

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
        self.select_model_submenu = self.options_menu.addMenu("Select machine learning model")
        self.select_model_sub_menu_action.setDefaultWidget(self.select_model_combo_box)
        self.select_model_submenu.addAction(self.select_model_sub_menu_action)
        #### Select model END

        self.options_menu.addAction(self.action_set_server)
        self.options_menu.addAction(self.toggle_action)

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
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.pushButton_21.clicked.connect(lambda: self.play_or_pause_cross_section(self.ui.pushButton_21))
        self.ui.pushButton_11.clicked.connect(self.analyze_a2c_and_a4c_videos)
        self.ui.label_23.setText("")
        self.ui.label_26.setText("Height:")
        self.ui.label_25.setText("Weight:")
        self.initClearAllCrossSections()

        for i in range(self.ui.horizontalLayout_3.count()):
            widget = self.ui.horizontalLayout_3.itemAt(i).widget()
            if widget:
                widget.setVisible(False)

    # Select the machine learning model type. Unified model or separate view model.
    def on_select_model(self, index):
        combo_box = self.sender()
        selected_option = combo_box.itemText(index)
        print(f"Selected Option: {selected_option} combobox[{index}] enum[{ModelType(selected_option).name}]")
        DataManager().model_type = ModelType(selected_option)

    # LVEF & LAV layout
    def toggle_layout_visibility(self):
        visible = self.ui.horizontalLayout_3.itemAt(0).widget().isVisible()
        for i in range(self.ui.horizontalLayout_3.count()):
            widget = self.ui.horizontalLayout_3.itemAt(i).widget()
            if widget:
                widget.setVisible(not visible)
        

    # Set the server address
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
    
    # button on click
    def analyze_a2c_and_a4c_videos(self):
        # Always use the one/five frame(s) results
        gridWidget = self.ui.gridWidget

        patient_editor_dialog = PatientEditor()
        patient_editor_dialog.patient_info_updated.connect(self.handle_patient_info)
        if not patient_editor_dialog.exec_() == QtWidgets.QDialog.Accepted:
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
            a2c_video = []
            a4c_video = []
            for frame_index in range(NUM_FRAMES):
                # Always use the one/five frame(s) results
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
                            if not view == "A2C" and not view == "A4C":
                                continue

                            _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result

                            ### Rotation
                            label = self.findLabel(view, gridWidget)
                            if hasattr(label, 'tag'):
                                degree = int(label.tag.split(",")[2])
                            else:
                                degree = 0
                            transform = QtGui.QTransform().rotate(degree)
                            annotated_qimage = annotated_qimage.transformed(transform)
                            ### Rotation END
                            width = annotated_qimage.width()
                            height = annotated_qimage.height()
                            annotated_qimage = annotated_qimage.convertToFormat(QtGui.QImage.Format_RGB32)
                            ptr = annotated_qimage.constBits()
                            numpy_frame = np.array(ptr).reshape(height, width, 4)  #  Copies the data
                            numpy_frame = numpy_frame[:, :, :3]
                            # Convert BGR to GRAY
                            numpy_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2GRAY)
                            if view == "A2C":
                                a2c_video.append(numpy_frame.tolist())
                            elif view == "A4C":
                                a4c_video.append(numpy_frame.tolist())
            
            a2c_video = np.array(a2c_video)
            a4c_video = np.array(a4c_video)
            print("a2c_video: ", a2c_video.shape)
            print("a4c_video: ", a4c_video.shape)

            t1 = threading.Thread(
                target=self.send_a2c_and_a4c_videos,
                args=(
                    a2c_video,
                    a4c_video,
                    self.ui,
                ),
            )
            t1.start()

        except Exception as e:
            print(e)

    # send 2 video streams to server
    def send_a2c_and_a4c_videos(self, a2c_video, a4c_video, ui):
            view_to_video = {
                "A2C": a2c_video,
                "A4C": a4c_video
            }

            pickled_data = pickle.dumps(view_to_video)
            compressed_data = blosc.compress(pickled_data)

            base_url = DataManager().server_base_url
            api = "analyze_a2c_and_a4c"
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
                    out_1d = pickle.loads(pickled_data)
                    array_string = np.array2string(out_1d)
                    print('LVEF & LAV: ', array_string)
                    display_string = 'LVEF: ' + str(round(out_1d[5], 2)) + '   LAV: ' + str(round(out_1d[2], 2))
                    ui.label_23.setText(display_string)

                else:
                    print("Error:", response.text)
                    loader = QtUiTools.QUiLoader()
                    ui_file = QtCore.QFile(resource_path("errordialog.ui"))
                    ui_file.open(QtCore.QFile.ReadOnly)
                    dialog = loader.load(ui_file)
                    dialog.label.setText("analyze_a2c_and_a4c")
                    dialog.label_2.setText("response is not 200")
                    dialog.exec_()
                    return
            except Exception as e:
                print(e)

    # export videos
    def export_all(self):
        dialog = QFileDialog()        
        folder_path = dialog.getExistingDirectory(self, "Select folder to save MP4 files")
       
        if folder_path == "":
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid folder!")
            dialog.label_2.setText("")
            dialog.exec_()
            return
        
        view_analyze_all_tab = self.ui.tabWidget.currentIndex() == 1
        gridWidget = self.ui.gridWidget_2 if view_analyze_all_tab else self.ui.gridWidget

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
                if view_analyze_all_tab:
                    all_results = DataManager().get_pred_result_analyze_all(0)
                else:
                    all_results = DataManager().get_pred_result(0)
                if not all_results == None:
                    for view, pred_result in all_results.items():
                        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result
                        ### Rotation
                        label = self.findLabel(view, gridWidget)
                        if hasattr(label, 'tag'):
                            degree = int(label.tag.split(",")[2])
                        else:
                            degree = 0
                        transform = QtGui.QTransform().rotate(degree)
                        annotated_qimage = annotated_qimage.transformed(transform)
                        ### Rotation END
                        width = annotated_qimage.width()
                        height = annotated_qimage.height()
                        output_file = os.path.join(folder_path, f"{view}.mp4")
                        frame_rate = int(DataManager().dicom_fps)
                        view_to_video_writer[view] = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (width, height))
            ## Save as video END
            for frame_index in range(NUM_FRAMES):
                if view_analyze_all_tab:
                    all_results = DataManager().get_pred_result_analyze_all(frame_index)
                else:
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
                            ### Rotation
                            label = self.findLabel(view, gridWidget)
                            if hasattr(label, 'tag'):
                                degree = int(label.tag.split(",")[2])
                            else:
                                degree = 0
                            transform = QtGui.QTransform().rotate(degree)
                            annotated_qimage = annotated_qimage.transformed(transform)
                            ### Rotation END
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

    # export images
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
        
        view_analyze_all_tab = self.ui.tabWidget.currentIndex() == 1
        gridWidget = self.ui.gridWidget_2 if view_analyze_all_tab else self.ui.gridWidget

        try:
            if view_analyze_all_tab:
                all_results = DataManager().get_pred_result_analyze_all(frame_index)
            else:
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

                        ### Rotation
                        label = self.findLabel(view, gridWidget)
                        if hasattr(label, 'tag'):
                            degree = int(label.tag.split(",")[2])
                        else:
                            degree = 0
                        transform = QtGui.QTransform().rotate(degree)
                        annotated_qimage = annotated_qimage.transformed(transform)
                        ### Rotation END

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

    # play/pause playing of frames
    def play_or_pause_cross_section(self, button):
        if self.is_playing(button) == None:
            print(f"Play/Pause button {button} is broken!")
            return
        elif self.is_playing(button) == False:
            old_style_sheet = self.ui.pushButton_21.styleSheet()
            new_style_sheet = old_style_sheet.replace(":/images/icons8-play-button-48.png", ":/images/icons8-pause-button-48.png")
            self.ui.pushButton_21.setStyleSheet(new_style_sheet)
            # self.ui.pushButton_21.setIcon(QIcon(resource_path('/resources/icons8-pause-button-48.png')))

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
            # self.ui.pushButton_21.setIcon(QIcon(resource_path('/resources/icons8-play-button-48.png')))

            self.play_timer.stop()

    # check if frames are playing
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

    def on_tab_changed(self, index):
        current_tab_index = index
        frame_index = self._current_frame_index
        self.refresh_cross_sections(frame_index, current_tab_index)

    def frame_index_changed(self, slider_value):
        # print(slider_value)
        frame_index: int = slider_value
        self._current_frame_index = frame_index

        current_tab_index = self.ui.tabWidget.currentIndex()
        self.refresh_cross_sections(frame_index, current_tab_index)

    # refresh UI display on tab and frame index
    def refresh_cross_sections(self, frame_index, current_tab_index):
        self.ui.label_10.setText(f"Selected time frame index: {frame_index}")

        view_analyze_all_tab = current_tab_index == 1
        gridWidget = self.ui.gridWidget_2 if view_analyze_all_tab else self.ui.gridWidget

        if view_analyze_all_tab:
            all_results = DataManager().get_pred_result_analyze_all(frame_index)
            all_center_images = DataManager().get_center_images_analyze_all(frame_index)
        else:
            all_results = DataManager().get_pred_result(frame_index)
            all_center_images = DataManager().get_center_images(frame_index)
        
        if all_results == None:
            gridWidget.setVisible(False)
        else:
            gridWidget.setVisible(True)

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

            if self.shouldInit(gridWidget):
                initAll = True
            else:
                initAll = False
            for view, pred_result in all_results.items():
                if pred_result == None:
                    print(f"At frame index {frame_index}, the pred_result for view {view} is None!")
                    # first_found_width = DataManager().get_result_width(view)
                    # if not first_found_width == None:
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
                            # print(f"Highlighted view: {view}")
                            brightness = 45.0
                        # else:
                            # print("Highlighted view does not match with the current")

                        ## Update OpenGL cross sections
                        crossSection3D = Quad(app, tex_id="skybox", pos=(gl_cx, gl_cy, gl_cz), rot=(rx - 90, ry, rz), brightness=brightness)
                        add(crossSection3D)
                        ####
                        
                        # DataManager().update_result_width(view, annotated_qimage.width())

                        if initAll:
                            self.addCrossSection(annotated_qimage, view, frame_index, gridWidget)
                        else:
                            self.modifyCrossSection(annotated_qimage, view, frame_index, gridWidget)
                    except Exception as e:
                        print(e)

    def handle_patient_info(self, height, weight):
        # print("Received patient info:")
        # print("Height:", height)
        # print("Weight:", weight)
        if not height == "":
            self.ui.label_26.setText(f"Height: {height}cm")
        if not weight == "":
            self.ui.label_25.setText(f"Weight: {weight}kg")

    def alert_removing_patient_data(self):
        if self._is_first_patient:
            self._is_first_patient = False
        else:
            # Alert
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(resource_path("errordialog.ui"))
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.setWindowTitle("Notification")
            dialog.label.setText("Any previous patient data, if exists,")
            dialog.label_2.setText("will be deleted")
            dialog.exec_()

    ''' Single Frame'''
    # on click
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
        
        self.alert_removing_patient_data()

        # Reset part 1
        if not self.read_dicom_thread == None:
            self.read_dicom_thread.stop()
        if not self.send_dicom_thread == None:
            self.send_dicom_thread.stop()
        
        if not self.process_dicom_thread == None:
            self.process_dicom_thread.stop()
        self.reset_results()
        ##

        # Reset part 1.1
        if not self.read_dicom_thread == None:
            self.read_dicom_thread.wait()

        self.read_dicom_thread = ReadDicomThread(filepath, self.ui)
        self.read_dicom_thread.finished.connect(self.handle_read_dicom_result_analyze_selected)
        self.read_dicom_thread.ui_update.connect(self.handle_read_dicom_ui_update)
        self.read_dicom_thread.start()

    # Starts thread to send data to server. SendDicomThread
    def handle_read_dicom_result_analyze_selected(self, serialized_data):
        print("handle_read_dicom_result_analyze_selected")

        # Reset part 1.2
        if not self.send_dicom_thread == None:
            self.send_dicom_thread.wait()

        self.send_dicom_thread = SendDicomThread(serialized_data, self.ui)
        self.send_dicom_thread.finished.connect(self.handle_send_dicom_result_analyze_selected)
        self.send_dicom_thread.ui_update.connect(self.handle_send_dicom_ui_update)
        self.send_dicom_thread.start()

    # callback for SendDicomThread. Start ProcessDicomThread thread. Analyze 1 frame
    def handle_send_dicom_result_analyze_selected(self, array_4d):
        print("handle_send_dicom_result_analyze_selected")

        # Reset part 2
        if not self.process_dicom_thread == None:
            self.process_dicom_thread.wait()
        ##

        self.process_dicom_thread = ProcessDicomThread(False, array_4d, self.ui, -1, False)
        self.process_dicom_thread.finished.connect(self.handle_process_dicom_result_analyze_selected)
        self.process_dicom_thread.ui_update.connect(self.handle_process_dicom_ui_update)
        self.process_dicom_thread.start()

    # called once simple predictions are all completed. Call detailed predictions
    def handle_process_dicom_result_analyze_selected(self, results):
        print("handle_process_dicom_result_analyze_selected")
        print(len(results))
        # self.handle_send_dicom_result_analyze_all(DataManager().data_4d_padded)
        self.handle_send_dicom_result_analyze_five_frames(DataManager().data_4d_padded)

    ''' 5 Frames '''
    ## No longer used. No longer in UI
    # on click
    def import_dicom_and_analyze_five_frames(self):
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Select DICOM File, in which five time frames will be analyzed"),
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
        
        self.alert_removing_patient_data()

        # Reset part 1
        if not self.read_dicom_thread == None:
            self.read_dicom_thread.stop()
        if not self.send_dicom_thread == None:
            self.send_dicom_thread.stop()
            
        if not self.process_dicom_thread == None:
            self.process_dicom_thread.stop()
        self.reset_results()
        ##
        
        # Reset part 1.1
        if not self.read_dicom_thread == None:
            self.read_dicom_thread.wait()
        
        self.read_dicom_thread = ReadDicomThread(filepath, self.ui)
        self.read_dicom_thread.finished.connect(self.handle_read_dicom_result_analyze_five_frames)
        self.read_dicom_thread.ui_update.connect(self.handle_read_dicom_ui_update)
        self.read_dicom_thread.start()

    # Starts thread to send data to server. SendDicomThread
    def handle_read_dicom_result_analyze_five_frames(self, serialized_data):
        print("handle_read_dicom_result_analyze_five_frames")
        
        # Reset part 1.2
        if not self.send_dicom_thread == None:
            self.send_dicom_thread.wait()

        self.send_dicom_thread = SendDicomThread(serialized_data, self.ui)
        self.send_dicom_thread.finished.connect(self.handle_send_dicom_result_analyze_five_frames)
        self.send_dicom_thread.ui_update.connect(self.handle_send_dicom_ui_update)
        self.send_dicom_thread.start()

    # callback for SendDicomThread. Start ProcessDicomThread thread. Analyze 5 frames
    def handle_send_dicom_result_analyze_five_frames(self, array_4d):
        print("handle_send_dicom_result_analyze_five_frames")

        # Reset part 2
        if not self.process_dicom_thread == None:
            self.process_dicom_thread.wait()
        ##

        self.process_dicom_thread = ProcessDicomThread(True, array_4d, self.ui, -1, True) # -1 = mid-point time frame
        self.process_dicom_thread.finished.connect(self.handle_process_dicom_result_analyze_five_frames)
        self.process_dicom_thread.ui_update.connect(self.handle_process_dicom_ui_update)
        self.process_dicom_thread.start()

    def handle_process_dicom_result_analyze_five_frames(self, results):
        print("handle_process_dicom_result_analyze_five_frames")
        print("results: ", len(results))
        pass
        # self.handle_send_dicom_result_analyze_all(DataManager().data_4d_padded)

    ''' All Frames '''
    ## No longer used. No longer in UI
    # on click
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
                
        self.read_dicom_thread = ReadDicomThread(filepath, self.ui)
        self.read_dicom_thread.finished.connect(self.handle_read_dicom_result_analyze_all)
        self.read_dicom_thread.ui_update.connect(self.handle_read_dicom_ui_update)
        self.read_dicom_thread.start()

    ## No longer used. No longer in UI
    def handle_read_dicom_result_analyze_all(self, serialized_data):
        print("handle_read_dicom_result_analyze_all")
        
        self.send_dicom_thread = SendDicomThread(serialized_data, self.ui)
        self.send_dicom_thread.finished.connect(self.handle_send_dicom_result_analyze_all)
        self.send_dicom_thread.ui_update.connect(self.handle_send_dicom_ui_update)
        self.send_dicom_thread.start()

    ## No longer used.
    # Start ProcessDicomThread thread. Analyze all frames
    def handle_send_dicom_result_analyze_all(self, array_4d):
        print("handle_send_dicom_result_analyze_all")

        self.process_dicom_thread = ProcessDicomThread(True, array_4d, self.ui, -1, False)
        self.process_dicom_thread.finished.connect(self.handle_process_dicom_result_analyze_all)
        self.process_dicom_thread.ui_update.connect(self.handle_process_dicom_ui_update)
        self.process_dicom_thread.start()

    ## No longer used
    def handle_process_dicom_result_analyze_all(self, results):
        print("handle_process_dicom_result_analyze_all")
        print(len(results))
        pass

    # endregion

    '''
    Reset when new patient data is fed
    '''
    def reset_results(self):
        print("reset_results")
        self.ui.label_26.setText(f"Height: ")
        self.ui.label_25.setText(f"Weight: ")
        self.ui.label_23.setText("")
        # Reset video info
        DataManager()._dicom_number_of_frames = -1
        DataManager()._dicom_average_frame_time_in_ms = 60.0
        DataManager()._dicom_fps = -1.0
        DataManager()._dicom_total_duration_in_s = -1.0
        self.ui.label_16.setText(f"Video - Number of Frames: ")
        self.ui.label_15.setText(f"Video - Average Frame Time: ")
        self.ui.label_9.setText(f"Video - FPS: ")
        self.ui.label_14.setText(f"Video - Total Duration: ")
        # Reset video info END
        self.ui.pushButton_11.setEnabled(False)
        DataManager().clear_pred_results_2()
        DataManager().clear_center_images_2()
        DataManager().clear_pred_results()
        DataManager().clear_center_images()
        frame_index = self._current_frame_index
        self.ui.horizontalSlider.setValue(0)
        self.ui.horizontalSlider.setValue(1)
        self.ui.horizontalSlider.setValue(frame_index)

    def handle_read_dicom_ui_update(self, function_and_args):
        print("handle_read_dicom_ui_update")
        function, *args = function_and_args
        # print(function)
        # print(args)
        function(*args)

    def handle_send_dicom_ui_update(self, function_and_args):
        print("handle_send_dicom_ui_update")
        function, *args = function_and_args
        # print(function)
        # print(args)
        function(*args)

    def handle_process_dicom_ui_update(self, function_and_args):
        # print("handle_process_dicom_ui_update")
        function, *args = function_and_args
        # print(function)
        # print(args)
        function(*args)

    def setHighlight(self, view, frame_index, always_highlight=False):
        view_analyze_all_tab = self.ui.tabWidget.currentIndex() == 1
    
        if not always_highlight and DataManager().highlighted_view == view:
            DataManager().highlighted_view = ""
        else:
            DataManager().highlighted_view = view
        if view_analyze_all_tab:
            all_results = DataManager().get_pred_result_analyze_all(frame_index)
            all_center_images = DataManager().get_center_images_analyze_all(frame_index)
        else:
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

    def export(self, view):
        view_analyze_all_tab = self.ui.tabWidget.currentIndex() == 1
        gridWidget = self.ui.gridWidget_2 if view_analyze_all_tab else self.ui.gridWidget
    
        ## Rotation
        frame_index = self._current_frame_index
        if view_analyze_all_tab:
            all_results = DataManager().get_pred_result_analyze_all(frame_index)
        else:
            all_results = DataManager().get_pred_result(frame_index)
        pred_result = all_results[view]
        _, _, annotated_qimage, rx, ry, rz, cx, cy, cz = pred_result
        label = self.findLabel(view, gridWidget)
        if hasattr(label, 'tag'):
            degree = int(label.tag.split(",")[2])
        else:
            degree = 0
        transform = QtGui.QTransform().rotate(degree)
        annotated_qimage.transformed(transform)
        ## Rotation END

        dialog = QFileDialog()
        dialog.setDefaultSuffix(".png")
        default_filename = f"frame-{frame_index}-view-{view}"
        file_path, _ = dialog.getSaveFileName(self, "Save PNG", default_filename, "PNG Files (*.png)")

        if file_path:
            ### Rotate
            transform = QtGui.QTransform().rotate(degree)
            annotated_qimage = annotated_qimage.transformed(transform)
            ### END
            annotated_qimage.save(f"{file_path}")
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

    def findLabel(self, view, gridWidget):
        grid_layout = gridWidget.layout()
        cross_section = self.findCrossSection(grid_layout, view)
        return cross_section.findChild(QLabel, "label_8")

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

    def modifyCrossSection(self, annotated_qimage, view, frame_index, gridWidget):
        grid_layout = gridWidget.layout()
        cross_section = self.findCrossSection(grid_layout, view)

        scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
        # print(f"scrollArea_width: {scrollArea_width}")
        new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N

        pixmap = QtGui.QPixmap.fromImage(annotated_qimage)
        label = cross_section.findChild(QLabel, "label_8")

        degree = int(label.tag.split(",")[2])
        transform = QtGui.QTransform().rotate(degree)
        pixmap = pixmap.transformed(transform)

        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label.setPixmap(pixmap)

        # if label.tag == "":
        #     label.tag = f"{view},{frame_index},0"
        # else:
        #     # TODO more serious error handling
        #     new_degree = (int(label.tag.split(",")[2]) - 90) % 360
        #     label.tag = f"{view},{frame_index},{new_degree}"
        label.tag = f"{view},{frame_index},{degree}"

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

    def shouldInit(self, gridWidget):
        count = gridWidget.layout().count()
        if count == 0:
            return True
        return False

    def addCrossSection(self, annotated_qimage, view, frame_index, gridWidget):
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
        label = cross_section.findChild(QLabel, "label_8")

        if hasattr(label, 'tag'):
            degree = int(label.tag.split(",")[2])
        else:
            degree = 0
        transform = QtGui.QTransform().rotate(degree)
        pixmap = pixmap.transformed(transform)

        pixmap = pixmap.scaledToWidth(new_pixmap_width)
        label.setPixmap(pixmap)

        # if label.tag == "":
        #     label.tag = f"{view},{frame_index},0"
        # else:
        #     # TODO more serious error handling
        #     new_degree = (int(label.tag.split(",")[2]) - 90) % 360
        #     label.tag = f"{view},{frame_index},{new_degree}"
        label.tag = f"{view},{frame_index},{degree}"

        label.show()

        view_button = cross_section.findChild(QPushButton, "pushButton_13")
        view_button.setText(view)
        view_button.clicked.connect(lambda: self.setHighlight(view, frame_index, always_highlight=False))
        # Also want ClickableQLabel to highlight the 3D plane, while always_highlight is True
        label.on_click = lambda: self.setHighlight(view, frame_index, always_highlight=True)

        export_button = cross_section.findChild(QPushButton, "pushButton_9")
        export_button.clicked.connect(lambda: self.export(view))

        counterclockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton")
        clockwise_rotate_button = cross_section.findChild(QPushButton, "pushButton_2")
        counterclockwise_rotate_button.clicked.connect(lambda: self.counterclockwiseRotate90(annotated_qimage, label, view, frame_index))
        clockwise_rotate_button.clicked.connect(lambda: self.clockwiseRotate90(annotated_qimage, label, view, frame_index))

        gridWidget.addWidget(cross_section)
        fixed_width = new_pixmap_width
        label.parent().setFixedWidth(fixed_width)
        label.setFixedHeight(fixed_width)

    # def addPlaceholderCrossSection(self, view):
    #     loader = QtUiTools.QUiLoader()
    #     loader.registerCustomWidget(ClickableQLabel)
    #     ui_file = QtCore.QFile(resource_path("crosssection.ui"))
    #     ui_file.open(QtCore.QFile.ReadOnly)
    #     cross_section = loader.load(ui_file)
    #     ui_file.close()

    #     scrollArea_width = self.ui.scrollAreaWidgetContents_3.width()
    #     # print(f"scrollArea_width: {scrollArea_width}")
    #     new_pixmap_width = (scrollArea_width - 18 - 12) / 3 # TODO change 3 to N

    #     pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(new_pixmap_width, 0, QtGui.QImage.Format_RGB888))
    #     label = cross_section.findChild(QLabel, "label_8")
    #     label.setPixmap(pixmap)
    #     label.show()

    #     view_button = cross_section.findChild(QPushButton, "pushButton_13")
    #     view_button.setText(view)

    #     self.ui.gridWidget.addWidget(cross_section)

    def initClearAllCrossSections(self):
        self.ui.gridWidget.clearAllItems(self.ui.gridWidget)
        self.ui.gridWidget_2.clearAllItems(self.ui.gridWidget_2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
