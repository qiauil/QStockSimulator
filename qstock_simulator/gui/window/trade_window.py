from .window_basics import  TitleMenuWindow
from qfluentwidgets import InfoBar, InfoBarPosition, FluentIcon, Action
from ..widget.control_pannel import ControlPannel
from ..widget.pips_pager_navigation import PipsPagerNavigation
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

class TradeWindow(TitleMenuWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent,main_lyout_direction="vertical")
        #self.main_layout.addWidget(SubtitleLabel("Stock Info",parent=self))
        self.stock_info_navigation = PipsPagerNavigation(parent=self)
        self.stock_info_navigation.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.stock_info_navigation)
        #self.main_layout.addWidget(SubtitleLabel("Control Pannel",parent=self))
        self.control_pannel = ControlPannel(parent=self)
        #self.control_pannel.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.control_pannel.setMaximumHeight(300)
        self.main_layout.addWidget(self.control_pannel)
        # menu

        self.state_info_action = Action("State info", parent=self)
        self.state_info_action.setIcon(FluentIcon.VIEW)
        def state_info_action_triggered():
            if self.control_pannel.info_plot_card.isVisible():
                self.control_pannel.info_plot_card.hide()
                self.state_info_action.setIcon(FluentIcon.HIDE)
            else:
                self.control_pannel.info_plot_card.show()
                self.state_info_action.setIcon(FluentIcon.VIEW)    
        self.state_info_action.triggered.connect(state_info_action_triggered)
        self.menu.addAction(self.state_info_action)

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