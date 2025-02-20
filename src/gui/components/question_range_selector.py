from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QSpinBox, QHBoxLayout, QPushButton)
from ..dialogs.config_popup import ConfigPopup

class QuestionRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Create range selection widgets
        range_layout = QHBoxLayout()
        self.start_spin = QSpinBox()
        self.end_spin = QSpinBox()
        
        range_layout.addWidget(QLabel("Question Range:"))
        range_layout.addWidget(self.start_spin)
        range_layout.addWidget(QLabel("to"))
        range_layout.addWidget(self.end_spin)
        
        # Configure button
        self.config_button = QPushButton("Configure Questions")
        self.config_button.clicked.connect(self.show_config)
        
        layout.addLayout(range_layout)
        layout.addWidget(self.config_button)
        self.setLayout(layout)
    
    def show_config(self):
        dialog = ConfigPopup(self.start_spin.value(), self.end_spin.value())
        dialog.exec_()