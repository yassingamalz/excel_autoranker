from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                           QLabel, QSpinBox, QHBoxLayout, QMessageBox)
from ..dialogs.dimension_preview import DimensionPreviewDialog
from ...utils.logger import AppLogger
import pandas as pd
import re

class DimensionConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = AppLogger.get_logger()
        self.file_path = None
        self.dimension_data = {}  # {dimension_number: [column_indices]}
        self.df = None
        self.setupUI()
        self.setEnabled(False)
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Info label
        self.info_label = QLabel("Dimensions will be automatically detected")
        
        # Dimensions summary label
        self.summary_label = QLabel("No dimensions detected")
        self.summary_label.setWordWrap(True)
        
        # Configure dimensions button
        self.config_button = QPushButton("Review Dimensions / مراجعة الأبعاد")
        self.config_button.clicked.connect(self.detect_dimensions)
        
        layout.addWidget(self.info_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.config_button)
        self.setLayout(layout)
    
    def set_file_path(self, file_path):
        """Set file path and load Excel file"""
        self.logger.info(f"Setting file path: {file_path}")
        self.file_path = file_path
        try:
            self.df = pd.read_excel(file_path)
            self.logger.info(f"Successfully loaded Excel file with {len(self.df.columns)} columns")
            self.detect_dimensions()
        except Exception as e:
            self.logger.error(f"Error loading file: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")

    def clean_column_name(self, col_name):
        """Clean column name and extract number"""
        try:
            # Extract first number from the column name
            match = re.search(r'^\d+', str(col_name))
            if match:
                return int(match.group())
            return None
        except Exception as e:
            self.logger.error(f"Error cleaning column name '{col_name}': {str(e)}")
            return None

    def detect_dimensions(self):
        """Automatically detect dimensions based on column numbering"""
        try:
            if not self.df is not None:
                self.logger.warning("No DataFrame available for dimension detection")
                return

            self.dimension_data.clear()
            current_dimension = []
            last_number = None
            
            self.logger.info("Starting dimension detection")
            
            for col_idx, col_name in enumerate(self.df.columns):
                number = self.clean_column_name(col_name)
                
                if number is None:
                    continue
                
                self.logger.debug(f"Processing column '{col_name}' with number {number}")
                
                # If we find a '1' or the number is less than the last number,
                # it's the start of a new dimension
                if number == 1 or (last_number and number < last_number):
                    if current_dimension:
                        dim_number = len(self.dimension_data) + 1
                        self.dimension_data[dim_number] = current_dimension
                        self.logger.info(f"Created dimension {dim_number} with {len(current_dimension)} columns")
                        current_dimension = []
                
                current_dimension.append(col_idx)
                last_number = number
            
            # Add the last dimension
            if current_dimension:
                dim_number = len(self.dimension_data) + 1
                self.dimension_data[dim_number] = current_dimension
                self.logger.info(f"Created final dimension {dim_number} with {len(current_dimension)} columns")
            
            self.update_summary()
            
        except Exception as e:
            self.logger.error(f"Error in dimension detection: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error detecting dimensions: {str(e)}")

    def update_summary(self):
        """Update the summary label with detected dimensions"""
        try:
            if not self.dimension_data:
                self.summary_label.setText("No dimensions detected")
                return
            
            summary = f"Detected {len(self.dimension_data)} dimensions:\n"
            
            for dim_num, columns in self.dimension_data.items():
                # Get the first and last column names for this dimension
                first_col = self.df.columns[columns[0]]
                last_col = self.df.columns[columns[-1]]
                count = len(columns)
                
                summary += f"\nDimension {dim_num}:\n"
                summary += f"- {count} questions\n"
                summary += f"- From: {first_col}\n"
                summary += f"- To: {last_col}\n"
            
            self.summary_label.setText(summary)
            self.logger.info(f"Updated dimension summary with {len(self.dimension_data)} dimensions")
            
        except Exception as e:
            self.logger.error(f"Error updating summary: {str(e)}")
            self.summary_label.setText("Error updating dimension summary")