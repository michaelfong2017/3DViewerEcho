# import sys
# from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PySide2.QtWidgets import QWidget, QGridLayout


class MyGridWidget(QWidget):
    def __init__(self, parent=None, num_elements=3):
        super().__init__(parent)
        self.num_elements = num_elements
        # self.layout = QGridLayout(self)

    def addWidget(self, widget):
        next_position = self.getNextAvailablePosition()
        self.layout().addWidget(widget, *next_position)

    def getNextAvailablePosition(self):
        for row in range(self.layout().rowCount() + 1):
            for column in range(self.num_elements):
                if not self.layout().itemAtPosition(row, column):
                    return row, column
        return self.layout().rowCount(), 0

    def clearAllItems(self, layout):
        while layout.layout().count():
            item = layout.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout:
                    self.clearAllItems(sublayout)


# if __name__ == "__main__":
#     # Create the application
#     app = QApplication(sys.argv)

#     # Create a window
#     window = QWidget()
#     window.setWindowTitle("MyGridWidget Example")

#     # Create a custom MyGridWidget
#     grid_widget = MyGridWidget(window, num_elements=3)
#     window.setLayout(grid_widget.layout)

#     # Create labels
#     label1 = QLabel("Label 1")
#     label2 = QLabel("Label 2")
#     label3 = QLabel("Label 3")
#     label4 = QLabel("Label 4")

#     # Add labels to the custom layout
#     grid_widget.addWidget(label1)
#     grid_widget.addWidget(label2)
#     grid_widget.addWidget(label3)
#     grid_widget.addWidget(label4)

#     # Show the window
#     window.show()

#     # Run the event loop
#     sys.exit(app.exec_())