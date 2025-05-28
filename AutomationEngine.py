import sys
from PySide6.QtWidgets import QApplication

from GUI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())