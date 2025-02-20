from PyQt5.QtCore import Qt

# Main window styles
WINDOW_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}
"""

# Component styles
BUTTON_STYLE = """
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #106ebe;
}
QPushButton:pressed {
    background-color: #005a9e;
}
"""

GROUP_BOX_STYLE = """
QGroupBox {
    border: 1px solid #cccccc;
    border-radius: 6px;
    margin-top: 1em;
    padding: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px;
}
"""

PROGRESS_BAR_STYLE = """
QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #0078d4;
    width: 10px;
}
"""

# Dialog styles
DIALOG_STYLE = """
QDialog {
    background-color: white;
}
"""

# Define alignments
LABEL_ALIGNMENT = Qt.AlignLeft | Qt.AlignVCenter

# Define sizes
BUTTON_MIN_WIDTH = 120
PROGRESS_BAR_HEIGHT = 20