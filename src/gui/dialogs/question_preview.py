# src/gui/dialogs/question_preview.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QPushButton, QHBoxLayout,
                           QLabel, QHeaderView)
from PyQt5.QtCore import Qt
import pandas as pd

class QuestionPreviewDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.selected_columns = []
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Select Questions / اختيار الأسئلة")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            "Select questions by clicking headers\n"
            "حدد الأسئلة بالنقر على رؤوس الجدول"
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
            
            self.table.setRowCount(min(100, len(df)))
            self.table.setColumnCount(len(df.columns))
            
            self.table.setHorizontalHeaderLabels(df.columns)
            header = self.table.horizontalHeader()
            header.setSectionsClickable(True)
            header.sectionClicked.connect(self.handleHeaderClick)
            
            for row in range(min(100, len(df))):
                for col in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[row, col]))
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