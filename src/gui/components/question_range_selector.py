from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QScrollArea, QMessageBox, QWidget)
from PyQt5.QtCore import Qt
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
        self.selection_label.setWordWrap(True)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(200)  # Set minimum height
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for questions
        self.question_details = QLabel("")
        self.question_details.setWordWrap(True)
        self.question_details.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }
        """)
        
        scroll.setWidget(self.question_details)
        
        layout.addWidget(self.config_button)
        layout.addWidget(self.selection_label)
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def clean_question_text(self, text):
        """Remove leading numbers and clean up the question text."""
        import re
        # Remove patterns like "1.", "1-", "1 ", etc.
        cleaned = re.sub(r'^\d+[\.\-\s]*', '', text.strip())
        # Remove any remaining leading numbers and dots
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
        cleaned = re.sub(r'^\d+\s*', '', cleaned)
        return cleaned.strip()
    
    def show_config(self):
        if not self.file_path:
            return
            
        try:
            dialog = QuestionPreviewDialog(self.file_path, self)
            if dialog.exec_() == QuestionPreviewDialog.Accepted:
                self.selected_questions = dialog.selected_columns
                self.update_selection_label()
        except Exception as e:
            self.logger.error(f"Error in show_config: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")

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
    
    def update_selection_label(self):
        try:
            if self.selected_questions:
                count = len(self.selected_questions)
                selected_cols = [self.df.columns[i] for i in self.selected_questions]
                cleaned_cols = [self.clean_question_text(col) for col in selected_cols]
                
                self.selection_label.setText(
                    f"Selected {count} questions / تم اختيار {count} سؤال"
                )
                
                details = "<p style='font-weight: bold;'>Selected questions:</p>"
                for i, question in enumerate(cleaned_cols, 1):
                    details += f"<p>{i}. {question}</p>"
                
                self.question_details.setText(details)
                self.logger.debug(f"Updated selection label with {count} cleaned questions")
                
            else:
                self.selection_label.setText("No questions selected / لم يتم اختيار الأسئلة")
                self.question_details.setText("")
                self.logger.debug("No questions selected")
                
        except Exception as e:
            self.logger.error(f"Error updating selection label: {str(e)}")
            self.selection_label.setText("Error updating selection / خطأ في التحديث")