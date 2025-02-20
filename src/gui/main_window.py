import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox
from .layouts.main_layout import MainLayout
from .utils.language_manager import LanguageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(LanguageManager.get_text('app_title'))
        self.setMinimumSize(800, 600)
        
        self.setupLanguageSelector()
        
        main_widget = MainLayout()
        self.setCentralWidget(main_widget)
    
    def setupLanguageSelector(self):
        lang_widget = QWidget()
        lang_layout = QVBoxLayout()
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English / العربية', 'العربية / English'])
        self.lang_combo.currentIndexChanged.connect(self.changeLanguage)
        
        lang_layout.addWidget(self.lang_combo)
        lang_widget.setLayout(lang_layout)
        
        self.statusBar().addPermanentWidget(lang_widget)
    
    def changeLanguage(self, index):
        lang = 'ar' if index == 1 else 'en'

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()

__all__ = ['run_app']