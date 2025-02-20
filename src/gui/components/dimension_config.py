from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QSpinBox)
from ..dialogs.dimension_popup import DimensionPopup

class DimensionConfig(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Number of dimensions
        dim_layout = QHBoxLayout()
        self.dim_spin = QSpinBox()
        self.dim_spin.setMinimum(1)
        dim_layout.addWidget(QLabel("Number of Dimensions:"))
        dim_layout.addWidget(self.dim_spin)
        
        # Configure dimensions button
        self.config_button = QPushButton("Configure Dimensions")
        self.config_button.clicked.connect(self.show_dimension_config)
        
        layout.addLayout(dim_layout)
        layout.addWidget(self.config_button)
        self.setLayout(layout)
    
    def show_dimension_config(self):
        dialog = DimensionPopup(self.dim_spin.value())
        dialog.exec_()