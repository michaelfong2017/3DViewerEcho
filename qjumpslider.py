from PySide2 import QtWidgets
 
class QJumpSlider(QtWidgets.QSlider):
    def __init__(self, parent = None):
        super(QJumpSlider, self).__init__(parent)
     
    def mousePressEvent(self, event):
        #Jump to click position
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
     
    def mouseMoveEvent(self, event):
        #Jump to pointer position while moving
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))