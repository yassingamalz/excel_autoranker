# src/gui/layouts/main_layout.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from ..components.file_selector import FileSelector
from ..components.question_range_selector import QuestionRangeSelector
from ..components.dimension_config import DimensionConfig
from ..components.data_cleaner import DataCleaner
from ..components.progress_indicator import ProgressIndicator

class MainLayout(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        self.file_selector = FileSelector()
        self.question_selector = QuestionRangeSelector()
        self.dimension_config = DimensionConfig()
        self.data_cleaner = DataCleaner()
        self.progress = ProgressIndicator()
        
        self.file_selector.file_selected.connect(self.handle_file_selection)
        
        layout.addWidget(self.file_selector)
        layout.addWidget(self.question_selector)
        layout.addWidget(self.dimension_config)
        layout.addWidget(self.data_cleaner)
        layout.addWidget(self.progress)
        
        self.setLayout(layout)
    
    def handle_file_selection(self, file_path):
        self.selected_file = file_path
        self.file_selected.emit(file_path)
        self.dimension_config.setEnabled(True)
        self.dimension_config.set_file_path(file_path)
