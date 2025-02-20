# src/gui/components/question_range_selector.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                           QLabel, QSpinBox, QHBoxLayout, QMessageBox)
from ..dialogs.question_preview import QuestionPreviewDialog
from ...utils.logger import AppLogger
import pandas as pd

class QuestionRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = AppLogger.get_logger()
        self.file_path = None
        self.selected_questions = []
        self.df = None
        self.setupUI()
        self.setEnabled(False)
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Configure button
        self.config_button = QPushButton("Select Questions / اختيار الأسئلة")
        self.config_button.clicked.connect(self.show_config)
        
        # Selected questions label
        self.selection_label = QLabel("No questions selected / لم يتم اختيار الأسئلة")
        
        # Add detailed question list
        self.question_details = QLabel("")
        
        layout.addWidget(self.config_button)
        layout.addWidget(self.selection_label)
        layout.addWidget(self.question_details)
        self.setLayout(layout)
    
    def set_file_path(self, file_path):
        self.logger.info(f"Setting file path: {file_path}")
        self.file_path = file_path
        try:
            self.df = pd.read_excel(file_path)
            self.logger.info(f"Successfully loaded Excel file with {len(self.df.columns)} columns")
            self.show_config()
        except Exception as e:
            self.logger.error(f"Error loading file: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")
    
    def show_config(self):
        if not self.file_path:
            self.logger.warning("Attempted to show config without file path")
            return
            
        try:
            self.logger.debug("Opening question preview dialog")
            dialog = QuestionPreviewDialog(self.file_path, self)
            if dialog.exec_() == QuestionPreviewDialog.Accepted:
                self.selected_questions = dialog.selected_columns
                self.logger.info(f"Selected {len(self.selected_questions)} questions")
                self.update_selection_label()
        except Exception as e:
            self.logger.error(f"Error in show_config: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")
    
    def update_selection_label(self):
        try:
            if self.selected_questions:
                count = len(self.selected_questions)
                # Get the actual column names for detailed display
                selected_cols = [self.df.columns[i] for i in self.selected_questions]
                
                # Update main label
                self.selection_label.setText(
                    f"Selected {count} questions / تم اختيار {count} سؤال"
                )
                
                # Update detailed list
                details = "Selected questions:\n"
                for i, col in enumerate(selected_cols, 1):
                    details += f"{i}. {col}\n"
                self.question_details.setText(details)
                
                self.logger.debug(f"Updated selection label with {count} questions")
                self.logger.debug(f"Selected columns: {selected_cols}")
            else:
                self.selection_label.setText("No questions selected / لم يتم اختيار الأسئلة")
                self.question_details.setText("")
                self.logger.debug("No questions selected")
        except Exception as e:
            self.logger.error(f"Error updating selection label: {str(e)}")
            self.selection_label.setText("Error updating selection / خطأ في التحديث")