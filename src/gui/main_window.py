import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from .layouts.main_layout import MainLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel AutoRanker 📊")
        self.setMinimumSize(800, 600)
        
        # Set main layout
        main_widget = MainLayout()
        self.setCentralWidget(main_widget)

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()