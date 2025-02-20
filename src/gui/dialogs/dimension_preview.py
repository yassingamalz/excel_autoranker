from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHBoxLayout,
                             QLabel, QHeaderView, QSpinBox)
from PyQt5.QtCore import Qt
import pandas as pd

class DimensionPreviewDialog(QDialog):
    def __init__(self, file_path, dimension_number=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.dimension_number = dimension_number
        self.selected_columns = []
        self.df = None
        self.setupUI()
        
    def setupUI(self):
        title = "Select Dimension Columns / اختر أعمدة البعد" if self.dimension_number is None else f"Select Columns for Dimension {self.dimension_number} / اختر أعمدة البعد {self.dimension_number}"
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            "Select columns for this dimension by clicking headers\n"
            "حدد الأعمدة لهذا البعد بالنقر على رؤوس الجدول"
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
            self.df = pd.read_excel(self.file_path)
            
            self.table.setRowCount(min(100, len(self.df)))
            self.table.setColumnCount(len(self.df.columns))
            
            self.table.setHorizontalHeaderLabels(self.df.columns)
            header = self.table.horizontalHeader()
            header.setSectionsClickable(True)
            header.sectionClicked.connect(self.handleHeaderClick)
            
            for row in range(min(100, len(self.df))):
                for col in range(len(self.df.columns)):
                    item = QTableWidgetItem(str(self.df.iloc[row, col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, col, item)
            
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error / خطأ", str(e))
            self.reject()
    
    def handleHeaderClick(self, column_index):
        if column_index in self.selected_columns:
            self.selected_columns.remove(column_index)
            self.table.horizontalHeaderItem(column_index).setBackground(Qt.white)
        else:
            self.selected_columns.append(column_index)
            self.table.horizontalHeaderItem(column_index).setBackground(Qt.lightGray)