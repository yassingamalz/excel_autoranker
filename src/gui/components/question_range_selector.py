
# src/gui/components/question_range_selector.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                           QLabel, QSpinBox, QHBoxLayout, QMessageBox)
from ..dialogs.question_preview import QuestionPreviewDialog
import pandas as pd

class QuestionRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.selected_questions = []
        self.setupUI()
        self.setEnabled(False)
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Configure button
        self.config_button = QPushButton("Select Questions / اختيار الأسئلة")
        self.config_button.clicked.connect(self.show_config)
        
        # Selected questions label
        self.selection_label = QLabel("No questions selected / لم يتم اختيار الأسئلة")
        
        layout.addWidget(self.config_button)
        layout.addWidget(self.selection_label)
        self.setLayout(layout)
    
    def set_file_path(self, file_path):
        self.file_path = file_path
        self.show_config()  # Automatically show question selection dialog
    
    def show_config(self):
        if not self.file_path:
            return
            
        try:
            dialog = QuestionPreviewDialog(self.file_path, self)
            if dialog.exec_() == QuestionPreviewDialog.Accepted:
                self.selected_questions = dialog.selected_columns
                self.update_selection_label()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")
    
    def update_selection_label(self):
        if self.selected_questions:
            count = len(self.selected_questions)
            self.selection_label.setText(f"Selected {count} questions / تم اختيار {count} سؤال")
        else:
            self.selection_label.setText("No questions selected / لم يتم اختيار الأسئلة")