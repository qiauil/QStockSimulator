from .window_basics import DefaultWindow, ProgressiveWindow
from qfluentwidgets import TitleLabel, SubtitleLabel, InfoBar, InfoBarPosition
from ..widget.control_pannel import ControlPannel
from ..widget.pips_pager_navigation import PipsPagerNavigation
from PyQt6.QtCore import Qt

class TradeWindow(ProgressiveWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent,main_lyout_direction="vertical")
        #self.main_layout.addWidget(SubtitleLabel("Stock Info",parent=self))
        self.stock_info_navigation = PipsPagerNavigation(parent=self)
        self.main_layout.addWidget(self.stock_info_navigation)
        #self.main_layout.addWidget(SubtitleLabel("Control Pannel",parent=self))
        self.control_pannel = ControlPannel(parent=self)
        self.control_pannel.setFixedHeight(300)
        self.main_layout.addWidget(self.control_pannel)

    def show_success_info(self,title:str,content:str):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )
    
    def show_error_info(self,title:str,content:str):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )
    
    def show_warning_info(self,title:str,content:str):
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = TradeWindow()
    window.show()
    sys.exit(app.exec())