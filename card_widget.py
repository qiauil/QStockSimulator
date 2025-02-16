from qstock_simulator.gui.window.start_window import StartWindow
from qfluentwidgets import setTheme, Theme

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())