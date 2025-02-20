# src/gui/layouts/main_layout.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.gui.components.file_selector import FileSelector
from src.gui.components.question_range_selector import QuestionRangeSelector
from src.gui.components.dimension_config import DimensionConfig
from src.gui.components.data_cleaner import DataCleaner
from src.gui.components.progress_indicator import ProgressIndicator
from src.core.analyzer import StatisticalAnalyzer

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
        self.question_selector.setEnabled(True)
        self.question_selector.set_file_path(file_path)
        self.dimension_config.setEnabled(True)
        self.dimension_config.set_file_path(file_path)
