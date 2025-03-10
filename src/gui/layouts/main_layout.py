# src/gui/layouts/main_layout.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QMessageBox, QApplication)
from PyQt5.QtCore import pyqtSignal
from src.gui.components.file_selector import FileSelector
from src.gui.components.question_range_selector import QuestionRangeSelector
from src.gui.components.dimension_config import DimensionConfig
from src.gui.components.data_cleaner import DataCleaner
from src.gui.components.progress_indicator import ProgressIndicator
from src.core.analyzer import StatisticalAnalyzer
import sys

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
        
        # Add analysis button
        self.analyze_button = QPushButton("Run Analysis / تشغيل التحليل")
        self.analyze_button.clicked.connect(self.run_analysis)
        self.analyze_button.setEnabled(False)
        
        self.file_selector.file_selected.connect(self.handle_file_selection)
        
        layout.addWidget(self.file_selector)
        layout.addWidget(self.question_selector)
        layout.addWidget(self.dimension_config)
        layout.addWidget(self.data_cleaner)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.progress)
        
        self.setLayout(layout)
    
    def handle_file_selection(self, file_path):
        self.selected_file = file_path
        self.file_selected.emit(file_path)
        self.question_selector.setEnabled(True)
        self.question_selector.set_file_path(file_path)
        self.dimension_config.setEnabled(True)
        self.dimension_config.set_file_path(file_path)
        self.analyze_button.setEnabled(True)
    
    def run_analysis(self):
        try:
            if not self.selected_file:
                raise ValueError("No file selected")
            
            if not hasattr(self.question_selector, 'selected_questions') or not self.question_selector.selected_questions:
                raise ValueError("No questions selected")
            
            if not hasattr(self.dimension_config, 'dimension_data') or not self.dimension_config.dimension_data:
                raise ValueError("No dimensions configured")
            
            self.progress.update_progress(10, "Starting analysis...")
            
            # Pass original dimension data directly
            analyzer = StatisticalAnalyzer(
                self.selected_file,
                self.question_selector.selected_questions,
                self.dimension_config.dimension_data
            )
            
            self.progress.update_progress(30, "Running statistical analysis...")
            
            # Run analysis and get output file
            output_file = analyzer.analyze_and_export()
            
            self.progress.update_progress(100, "Analysis complete!")
            
            QMessageBox.information(
                self,
                "Analysis Complete / اكتمل التحليل",
                f"Results saved to:\n{output_file}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error / خطأ",
                str(e)
            )
            self.progress.update_progress(0, "Analysis failed")