from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from ..utils.language_manager import LanguageManager
from .excel_preview_dialog import ExcelPreviewDialog

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.file_label = QLabel(LanguageManager.get_text('no_file'))
        self.select_button = QPushButton(LanguageManager.get_text('file_select'))
        self.select_button.clicked.connect(self.select_file)
        
        layout.addWidget(self.file_label)
        layout.addWidget(self.select_button)
        self.setLayout(layout)
    
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            LanguageManager.get_text('file_select'),
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_name:
            preview_dialog = ExcelPreviewDialog(file_name, self)
            if preview_dialog.exec_() == ExcelPreviewDialog.Accepted:
                self.file_label.setText(file_name)
                self.selected_columns = preview_dialog.selected_columns