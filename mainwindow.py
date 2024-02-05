import sys
from PySide2 import QtGui, QtUiTools, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QAction, QMenu
from ui_mainwindow import Ui_MainWindow
import os
import threading
from dicomprocessor import process_dicom
from datamanager import DataManager
from clickableqlabel import ClickableQLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #### Top Menu Bar BEGIN ####
        # Create actions
        self.action_import_all_time_frame = QAction("Analyze all time frames", self)
        self.action_import_selected_time_frame = QAction("Analyze only the selected time frame", self)

        ### Export all cross-section images in all time frames
        self.action_export_all_cross_section_all_time_frames = QAction("Export all cross-section images in all time frames", self)
        ### Export all cross-section images in the current time frame
        self.action_export_all_cross_section_selected_time_frame = QAction("Export all cross-section images in the current time frame", self)

        # Connect actions to slots
        self.action_import_all_time_frame.triggered.connect(self.import_dicom_and_analyze_all)
        self.action_import_selected_time_frame.triggered.connect(self.import_dicom_and_analyze_selected)

        self.action_export_all_cross_section_all_time_frames.triggered.connect(self.export_all)
        self.action_export_all_cross_section_selected_time_frame.triggered.connect(self.export_selected_time_frame)

        # Create menus
        self.import_menu = QMenu("Import and Process DICOM file", self)
        self.import_menu.addAction(self.action_import_all_time_frame)
        self.import_menu.addAction(self.action_import_selected_time_frame)

        self.export_menu = QMenu("Export cross-section images", self)
        self.export_menu.addAction(self.action_export_all_cross_section_all_time_frames)
        self.export_menu.addAction(self.action_export_all_cross_section_selected_time_frame)
        
        # Create menu bar
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(self.import_menu)
        self.menu_bar.addMenu(self.export_menu)

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
        self.ui.gridWidget.clearAllItems(self.ui.gridWidget)

    def export_all(self):
        # TODO
        print("export_all")

    def export_selected_time_frame(self):
        # TODO
        print("export_selected_time_frame")

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
        self.ui.label_10.setText(f"Selected time frame index: {frame_index}")

        all_results = DataManager().get_pred_result(frame_index)
        
        self.clearAllCrossSections()

        if not all_results == None:
            i = 0
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
                        _, _, annotated_qimage = pred_result
                        
                        DataManager().update_result_width(view, annotated_qimage.width())

                        self.addCrossSection(annotated_qimage, view, frame_index)
                    except Exception as e:
                        print(e)

                i = i + 1

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
            ui_file = QtCore.QFile("errordialog.ui")
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid filepath!")
            dialog.label_2.setText("")
            dialog.exec_()
            return

        t1 = threading.Thread(
            target=process_dicom,
            args=(
                True,
                filepath,
                self.ui,
                -1,
            ),
        )
        t1.start()

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
            ui_file = QtCore.QFile("errordialog.ui")
            ui_file.open(QtCore.QFile.ReadOnly)
            dialog = loader.load(ui_file)
            dialog.label.setText("Please select a valid filepath!")
            dialog.label_2.setText("")
            dialog.exec_()
            return

        t1 = threading.Thread(
            target=process_dicom,
            args=(
                False,
                filepath,
                self.ui,
                self.ui.horizontalSlider.value(),
            ),
        )
        t1.start()
    
    def export(self, annotated_qimage, view, frame_index):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".png")
        default_filename = f"frame-{frame_index}-view-{view}"
        file_path, _ = dialog.getSaveFileName(self, "Save PNG", default_filename, "PNG Files (*.png)")

        if file_path:
            annotated_qimage.save(f"{file_path}.png")
            print("File saved successfully.")

    def addCrossSection(self, annotated_qimage, view, frame_index):
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(ClickableQLabel)
        ui_file = QtCore.QFile("crosssection.ui")
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
        label.tag = f"{view},{frame_index}"
        label.show()

        view_button = cross_section.findChild(QPushButton, "pushButton_13")
        view_button.setText(view)

        export_button = cross_section.findChild(QPushButton, "pushButton_9")
        export_button.clicked.connect(lambda: self.export(annotated_qimage, view, frame_index))

        self.ui.gridWidget.addWidget(cross_section)
        fixed_width = new_pixmap_width
        label.parent().setFixedWidth(fixed_width)
        label.setFixedHeight(fixed_width)

    def addPlaceholderCrossSection(self, view):
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(ClickableQLabel)
        ui_file = QtCore.QFile("crosssection.ui")
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
