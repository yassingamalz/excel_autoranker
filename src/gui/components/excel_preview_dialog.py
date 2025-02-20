from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHBoxLayout,
                             QLabel, QHeaderView)
from PyQt5.QtCore import Qt
import pandas as pd

class ExcelPreviewDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.selected_columns = []
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Excel Preview / معاينة ملف إكسل")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Instructions label
        instructions = QLabel(
            "Select columns by clicking on headers\n"
            "حدد الأعمدة بالنقر على رؤوس الجدول"
        )
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Excel preview table
        self.table = QTableWidget()
        self.loadExcelData()
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK / موافق")
        self.cancel_button = QPushButton("Cancel / إلغاء")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def loadExcelData(self):
        try:
            df = pd.read_excel(self.file_path)
            
            # Set up table
            self.table.setRowCount(min(100, len(df)))  # Show first 100 rows
            self.table.setColumnCount(len(df.columns))
            
            # Set headers
            self.table.setHorizontalHeaderLabels(df.columns)
            header = self.table.horizontalHeader()
            header.setSectionsClickable(True)
            header.sectionClicked.connect(self.handleHeaderClick)
            
            # Populate data
            for row in range(min(100, len(df))):
                for col in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[row, col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                    self.table.setItem(row, col, item)
            
            # Auto-adjust columns
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Error / خطأ",
                f"Failed to load Excel file / فشل تحميل ملف الإكسل\n{str(e)}"
            )
            self.reject()
    
    def handleHeaderClick(self, column_index):
        header = self.table.horizontalHeader()
        if column_index in self.selected_columns:
            self.selected_columns.remove(column_index)
            header.setSectionResizeMode(column_index, QHeaderView.Interactive)
        else:
            self.selected_columns.append(column_index)
            header.setSectionResizeMode(column_index, QHeaderView.Fixed)
        
        # Update visual feedback
        for col in range(self.table.columnCount()):
            if col in self.selected_columns:
                self.table.horizontalHeaderItem(col).setBackground(Qt.lightGray)
            else:
                self.table.horizontalHeaderItem(col).setBackground(Qt.white)