from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, 
                             QLabel, QGroupBox)

class DataCleaner(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Create group box for data cleaning options
        group_box = QGroupBox("Data Cleaning Options")
        group_layout = QVBoxLayout()
        
        # Cleaning options
        self.clean_checkbox = QCheckBox("Data needs cleaning")
        self.clean_checkbox.stateChanged.connect(self.toggle_mapping)
        
        # Mapping explanation
        mapping_label = QLabel(
            "Arabic text mapping:\n"
            "مكتسبة بشكل كامل = 3\n"
            "مكتسبة بدرجة متوسطة = 2\n"
            "غير مكتسبة = 1"
        )
        mapping_label.setVisible(False)
        self.mapping_label = mapping_label
        
        group_layout.addWidget(self.clean_checkbox)
        group_layout.addWidget(mapping_label)
        group_box.setLayout(group_layout)
        
        layout.addWidget(group_box)
        self.setLayout(layout)
    
    def toggle_mapping(self, state):
        self.mapping_label.setVisible(state == 2)  # 2 = Checked