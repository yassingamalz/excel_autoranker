from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QListWidget)

class ConfigPopup(QDialog):
    def __init__(self, start_q, end_q):
        super().__init__()
        self.setWindowTitle("Configure Questions")
        layout = QVBoxLayout()
        
        # Question list
        self.question_list = QListWidget()
        for i in range(start_q, end_q + 1):
            self.question_list.addItem(f"Question {i}")
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # Add widgets to layout
        layout.addWidget(QLabel("Select Questions:"))
        layout.addWidget(self.question_list)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)