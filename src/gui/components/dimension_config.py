from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                          QDialog, QTabWidget, QTextEdit, QHBoxLayout,
                          QMessageBox)
from ...utils.logger import AppLogger
import pandas as pd
import re

class DimensionPreviewDialog(QDialog):
   def __init__(self, dimensions_data, df, parent=None):
       super().__init__(parent)
       self.setWindowTitle("Dimensions Preview / معاينة الأبعاد")
       self.setMinimumSize(800, 600)
       
       layout = QVBoxLayout()
       
       # Create tab widget
       tabs = QTabWidget()
       
       # Create a tab for each dimension
       for dim_num, columns in dimensions_data.items():
           tab = QWidget()
           tab_layout = QVBoxLayout()
           
           # Create text display for questions
           questions_text = QTextEdit()
           questions_text.setReadOnly(True)
           
           # Add questions without the original numbering
           content = ""
           for i, col_idx in enumerate(columns, 1):
               # Clean up the column name by removing leading numbers
               col_name = df.columns[col_idx]
               cleaned_name = re.sub(r'^\d+[\-\.\)]\s*', '', str(col_name).strip())
               content += f"{i}. {cleaned_name}\n"
           
           questions_text.setText(content)
           tab_layout.addWidget(questions_text)
           tab.setLayout(tab_layout)
           
           tabs.addTab(tab, f"Dimension {dim_num} / البعد {dim_num}")
       
       layout.addWidget(tabs)
       
       # Add OK button
       ok_button = QPushButton("OK / موافق")
       ok_button.clicked.connect(self.accept)
       layout.addWidget(ok_button)
       
       self.setLayout(layout)

class DimensionConfig(QWidget):
   def __init__(self):
       super().__init__()
       self.logger = AppLogger.get_logger()
       self.file_path = None
       self.dimension_data = {}
       self.df = None
       self.setupUI()
       self.setEnabled(False)
       
   def setupUI(self):
       layout = QVBoxLayout()
       
       # Only keep the preview button
       self.preview_button = QPushButton("Preview Dimensions / معاينة الأبعاد")
       self.preview_button.clicked.connect(self.show_preview)
       self.preview_button.setEnabled(False)
       
       layout.addWidget(self.preview_button)
       self.setLayout(layout)
   
   def set_file_path(self, file_path):
       self.logger.info(f"Setting file path: {file_path}")
       self.file_path = file_path
       try:
           self.df = pd.read_excel(file_path)
           self.logger.info(f"Successfully loaded Excel file with {len(self.df.columns)} columns")
           self.detect_dimensions()
       except Exception as e:
           self.logger.error(f"Error loading file: {str(e)}")
           QMessageBox.critical(self, "Error", f"Error loading file: {str(e)}")

   def detect_dimensions(self):
       try:
           if self.df is None:
               return

           self.dimension_data.clear()
           current_dimension = []
           last_number = None
           
           for col_idx, col_name in enumerate(self.df.columns):
               # Extract first number from column name
               match = re.search(r'^\d+', str(col_name))
               if not match:
                   continue
                   
               number = int(match.group())
               
               if number == 1 or (last_number and number < last_number):
                   if current_dimension:
                       dim_number = len(self.dimension_data) + 1
                       self.dimension_data[dim_number] = current_dimension
                       current_dimension = []
               
               current_dimension.append(col_idx)
               last_number = number
           
           # Add final dimension
           if current_dimension:
               dim_number = len(self.dimension_data) + 1
               self.dimension_data[dim_number] = current_dimension
           
           self.preview_button.setEnabled(True)
           self.logger.info(f"Detected {len(self.dimension_data)} dimensions")
           
       except Exception as e:
           self.logger.error(f"Error detecting dimensions: {str(e)}")
           QMessageBox.critical(self, "Error", f"Error detecting dimensions: {str(e)}")

   def show_preview(self):
       try:
           if not self.dimension_data:
               return
               
           dialog = DimensionPreviewDialog(self.dimension_data, self.df, self)
           dialog.exec_()
           
       except Exception as e:
           self.logger.error(f"Error showing preview: {str(e)}")
           QMessageBox.critical(self, "Error", f"Error showing preview: {str(e)}")