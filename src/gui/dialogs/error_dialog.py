from PyQt5.QtWidgets import QMessageBox

class ErrorDialog:
    @staticmethod
    def show_error(title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()