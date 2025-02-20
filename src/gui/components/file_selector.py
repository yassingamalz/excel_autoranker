from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFileDialog
from ..utils.validators import validate_excel_file

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.select_button = QPushButton("Select Excel File")
        self.select_button.clicked.connect(self.select_file)
        
        layout.addWidget(self.file_label)
        layout.addWidget(self.select_button)
        self.setLayout(layout)
    
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_name and validate_excel_file(file_name):
            self.file_label.setText(file_name)
            # Emit signal for file selected