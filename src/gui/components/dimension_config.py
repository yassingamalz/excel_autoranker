
# src/gui/components/dimension_config.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QSpinBox, QHBoxLayout)
from ..dialogs.dimension_preview import DimensionPreviewDialog

class DimensionConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.dimension_data = {}
        self.setupUI()
        self.setEnabled(False)
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        dim_layout = QHBoxLayout()
        self.dim_spin = QSpinBox()
        self.dim_spin.setMinimum(1)
        self.dim_spin.setMaximum(10)
        
        dim_layout.addWidget(QLabel("Number of Dimensions / عدد الأبعاد:"))
        dim_layout.addWidget(self.dim_spin)
        
        self.config_button = QPushButton("Configure Dimensions / تكوين الأبعاد")
        self.config_button.clicked.connect(self.configureDimensions)
        
        layout.addLayout(dim_layout)
        layout.addWidget(self.config_button)
        self.setLayout(layout)
    
    def set_file_path(self, file_path):
        self.file_path = file_path
    
    def configureDimensions(self):
        if not self.file_path:
            return
            
        num_dimensions = self.dim_spin.value()
        self.dimension_data.clear()
        
        for dim in range(1, num_dimensions + 1):
            dialog = DimensionPreviewDialog(self.file_path, dim, self)
            if dialog.exec_() == DimensionPreviewDialog.Accepted:
                self.dimension_data[dim] = dialog.selected_columns
            else:
                break