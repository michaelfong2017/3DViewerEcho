from PySide2.QtCore import Signal
from PySide2.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide2.QtGui import QIntValidator, QDoubleValidator

class PatientEditor(QDialog):
    # Define a custom signal
    patient_info_updated = Signal(str, str)

    def __init__(self):
        super().__init__()

        # Set the window title as the instruction
        self.setWindowTitle("Please enter patient info:")

        # Create QLabel widgets for displaying the current height and weight
        self.height_label = QLabel("Height (cm): <span style='color:gray;'>(optional)</span>")
        self.weight_label = QLabel("Weight (kg): <span style='color:gray;'>(optional)</span>")

        # Create QLineEdit widgets for editing the height and weight
        self.height_edit = QLineEdit()
        self.weight_edit = QLineEdit()

        # Set validators to accept numbers only
        self.height_edit.setValidator(QDoubleValidator())
        self.weight_edit.setValidator(QDoubleValidator())

        # Create a QPushButton for saving the changes
        self.save_button = QPushButton("Save")

        # Connect the save_button clicked signal to a slot
        self.save_button.clicked.connect(self.save_changes)

        # Create a QVBoxLayout to arrange the widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_edit)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_edit)
        layout.addWidget(self.save_button)

        # Set the QVBoxLayout as the layout for the QDialog
        self.setLayout(layout)

        # Set the fixed width of the dialog
        self.setMinimumWidth(300)  # Adjust the value as per your requirement

    def save_changes(self):
        # Get the updated height and weight values from the QLineEdit widgets
        new_height = self.height_edit.text()
        new_weight = self.weight_edit.text()

        # Perform the necessary operations to save the changes to the patient's information
        # For example, you can update a database or store the values in variables

        # Print the updated height and weight
        # print("New Height:", new_height)
        # print("New Weight:", new_weight)

        # Emit the patient_info_updated signal with the updated values
        self.patient_info_updated.emit(new_height, new_weight)

        # Close the dialog
        self.accept()