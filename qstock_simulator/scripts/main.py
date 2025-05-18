from PyQt6.QtCore import Qt
import sys, os
from PyQt6.QtWidgets import QApplication
import argparse
from qstock_simulator.libs.config import cfg
from qstock_simulator.apps import (
    StartUpWindow,
    ProjectCreatorWindow,
    ProjectLoaderWindow,
    SettingWindow,
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run main program for QStockSimulator.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="startup",
        choices=["startup", "new", "load", "setup"],
        required=False,
        help="Mode to run the program.  Options are 'startup', 'new', 'load', and 'setup'.",
    )
    args = parser.parse_args()
    return args

def qstock():
    args=parse_args()
    if args.mode == "startup":
        window = StartUpWindow
    elif args.mode == "new":
        window = ProjectCreatorWindow
    elif args.mode == "load":
        window = ProjectLoaderWindow
    elif args.mode == "setup":
        window = SettingWindow
    else:
        raise ValueError("Invalid mode. Choose from 'startup', 'new', 'load', or 'setup'.")
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    window = window()
    window.show()
    sys.exit(app.exec())
