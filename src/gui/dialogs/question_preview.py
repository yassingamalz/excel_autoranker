# src/gui/dialogs/question_preview.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QPushButton, QHBoxLayout,
                           QLabel, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from ...utils.logger import AppLogger
import pandas as pd

class QuestionPreviewDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.logger = AppLogger.get_logger()
        self.file_path = file_path
        self.selected_columns = []
        self.df = None
        self.range_start = None
        self.range_complete = False
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Select Questions / اختيار الأسئلة")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            "Click first column to start range, then click last column to complete selection\n"
            "انقر على العمود الأول لبدء النطاق، ثم انقر على العمود الأخير لإكمال التحديد"
        )
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Selection status
        self.selection_status = QLabel("Click first column / انقر على العمود الأول")
        self.selection_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selection_status)
        
        # Excel preview table
        self.table = QTableWidget()
        self.loadExcelData()
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK / موافق")
        self.cancel_button = QPushButton("Cancel / إلغاء")
        self.clear_button = QPushButton("Clear Selection / مسح التحديد")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.clear_button.clicked.connect(self.clearSelection)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def loadExcelData(self):
        try:
            self.logger.info(f"Loading Excel file: {self.file_path}")
            self.df = pd.read_excel(self.file_path)
            self.logger.debug(f"Excel file loaded with {len(self.df.columns)} columns")
            
            self.table.setRowCount(min(100, len(self.df)))
            self.table.setColumnCount(len(self.df.columns))
            
            # Set headers
            self.table.setHorizontalHeaderLabels(self.df.columns)
            header = self.table.horizontalHeader()
            header.setSectionsClickable(True)
            header.sectionClicked.connect(self.handleHeaderClick)
            
            # Populate data
            for row in range(min(100, len(self.df))):
                for col in range(len(self.df.columns)):
                    item = QTableWidgetItem(str(self.df.iloc[row, col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
            self.logger.info("Excel data loaded successfully into table")
            
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {str(e)}")
            QMessageBox.critical(self, "Error / خطأ", str(e))
            self.reject()

    def handleHeaderClick(self, column_index):
        try:
            self.logger.debug(f"Column clicked: {column_index}")
            self.logger.debug(f"Current state - range_start: {self.range_start}, range_complete: {self.range_complete}")

            # If this is a new selection after a complete one, clear first
            if self.range_complete:
                self.clearSelection()

            if self.range_start is None:
                # First click
                self.range_start = column_index
                self.table.horizontalHeaderItem(column_index).setBackground(Qt.yellow)
                self.selection_status.setText("Now click last column / الآن انقر على العمود الأخير")
                self.logger.info(f"First column selected: {column_index}")
                return

            if self.range_start == column_index:
                self.logger.debug("Same column clicked - ignoring")
                return

            # Second click
            range_end = column_index
            start = min(self.range_start, range_end)
            end = max(self.range_start, range_end)
            
            self.logger.info(f"Range selected: {start} -> {end}")
            
            # Create the range
            self.selected_columns = list(range(start, end + 1))
            self.logger.info(f"Selected columns: {self.selected_columns}")
            
            # Update display
            for col in range(self.table.columnCount()):
                if col >= start and col <= end:
                    self.table.horizontalHeaderItem(col).setBackground(Qt.lightGray)
                else:
                    self.table.horizontalHeaderItem(col).setBackground(Qt.white)
            
            count = len(self.selected_columns)
            self.selection_status.setText(f"Selected {count} columns / تم اختيار {count} عمود")
            self.range_complete = True
            self.logger.info(f"Selection complete - {count} columns selected")
            
        except Exception as e:
            self.logger.error(f"Error in header click: {str(e)}")
            self.clearSelection()

    def clearSelection(self):
        try:
            self.logger.info("Clearing selection...")
            self.logger.debug(f"Before clear - range_start: {self.range_start}, range_complete: {self.range_complete}")
            
            self.range_start = None
            self.range_complete = False
            self.selected_columns = []
            
            # Reset all column backgrounds
            for col in range(self.table.columnCount()):
                self.table.horizontalHeaderItem(col).setBackground(Qt.white)
            
            self.selection_status.setText("Click first column / انقر على العمود الأول")
            self.logger.info("Selection cleared successfully")
        except Exception as e:
            self.logger.error(f"Error clearing selection: {str(e)}")

    def accept(self):
        self.logger.debug(f"Accept clicked - range_complete: {self.range_complete}, selected_columns: {self.selected_columns}")
        if self.range_complete and self.selected_columns:
            self.logger.info(f"Selection accepted: {len(self.selected_columns)} columns selected")
            super().accept()
        else:
            self.logger.warning("Accept clicked without complete selection")
            QMessageBox.warning(
                self,
                "Warning / تحذير",
                "Please select a complete range (first and last column)\n"
                "الرجاء تحديد النطاق كاملاً (العمود الأول والأخير)"
            )