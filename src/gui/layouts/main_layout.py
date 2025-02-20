from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ..components.file_selector import FileSelector
from ..components.question_range_selector import QuestionRangeSelector
from ..components.dimension_config import DimensionConfig
from ..components.data_cleaner import DataCleaner
from ..components.progress_indicator import ProgressIndicator

class MainLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Add components
        self.file_selector = FileSelector()
        self.question_selector = QuestionRangeSelector()
        self.dimension_config = DimensionConfig()
        self.data_cleaner = DataCleaner()
        self.progress = ProgressIndicator()
        
        # Add widgets to layout
        layout.addWidget(self.file_selector)
        layout.addWidget(self.question_selector)
        layout.addWidget(self.dimension_config)
        layout.addWidget(self.data_cleaner)
        layout.addWidget(self.progress)
        
        self.setLayout(layout)