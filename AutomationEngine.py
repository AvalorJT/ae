import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication # NEW: Import QGuiApplication
from PySide6.QtCore import Qt # NEW: Import Qt for the policy enum

from GUI.MainWindow import MainWindow

QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())