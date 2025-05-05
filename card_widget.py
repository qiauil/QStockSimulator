from qstock_simulator.libs.config import cfg
from qstock_simulator.apps.start_up import StartUpWindow
from qfluentwidgets import setTheme, Theme
from PyQt6.QtCore import Qt

if __name__ == "__main__":
    import sys,os
    from PyQt6.QtWidgets import QApplication
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    window = StartUpWindow()
    window.show()
    sys.exit(app.exec())