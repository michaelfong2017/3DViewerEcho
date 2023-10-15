# 3DViewerEcho
```
python -m venv venv
. venv/bin/activate
```

```bash
pip install --upgrade pip
pip install PySide2

pip install numpy
pip install Pillow
pip install moderngl

pip install moderngl
# moderngl_window for testing
pip install moderngl_window
pip install PyOpenGL PyOpenGL_accelerate
pip install PyGLM
pip install scipy

pip install vtk pydicom pynrrd
pip install cupy-cuda11x

pip install requests
pip install blosc

pip install plotly
```

```
pyside2-uic mainwindow.ui > ui_mainwindow.py
pyside2-uic crosssection.ui > ui_crosssection.py
pyside2-rcc resources/mainwindow.qrc -o mainwindow_rc.py
```

```
python mainwindow.py
```

# Functional design
1. Upon clicking the "Import DICOM file" button, the 3D heart and all its cross sections of the default time frame will be loaded.

2. Upon moving the "Select time frame" slidebar, the 3D heart and all its cross sections will be updated to the selected time frame.

3. Upon clicking the "Export as PNG" button, the individual cross-section image will be saved.

4. Upon selecting a cross section, the cross section plane and the three landmarks will be loaded to the 3D heart, and the selected cross section will be highlighted. User can then drag and drop to edit the landmarks, and the cross section plane will update accordingly.

5. Upon clicking the "Save edited landmarks to the current cross-section" button, the current cross section image will be updated.

6. "Export all cross-section images in the current time frame" button, as described.

7. "Export all cross-section images in all time frames" button, as described.
