from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel

class ProgressIndicator(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
    
    def update_progress(self, value, status):
        self.progress_bar.setValue(value)
        self.status_label.setText(status)