from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QSpinBox, QPushButton, QWidget)

class DimensionPopup(QDialog):
    def __init__(self, num_dimensions):
        super().__init__()
        self.setWindowTitle("Configure Dimensions")
        layout = QVBoxLayout()
        
        self.dimension_widgets = []
        
        # Create range inputs for each dimension
        for i in range(num_dimensions):
            dim_widget = QWidget()
            dim_layout = QHBoxLayout()
            
            dim_label = QLabel(f"Dimension {i+1} Range:")
            start_spin = QSpinBox()
            end_spin = QSpinBox()
            
            dim_layout.addWidget(dim_label)
            dim_layout.addWidget(start_spin)
            dim_layout.addWidget(QLabel("to"))
            dim_layout.addWidget(end_spin)
            
            dim_widget.setLayout(dim_layout)
            self.dimension_widgets.append((start_spin, end_spin))
            layout.addWidget(dim_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)