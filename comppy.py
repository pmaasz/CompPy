#!/usr/bin/env python3
"""
CompPy - Compressor Design Application
Entry point for running the application
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from MainWindow import Ui_MainWindow
except ImportError as e:
    print("Error: Required dependencies not installed.")
    print(f"Details: {e}")
    print("\nPlease install dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
