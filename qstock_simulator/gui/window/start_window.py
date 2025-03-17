from qfluentwidgets import FluentWindow, BodyLabel, FluentIcon,NavigationItemPosition
from ...libs.style import Icon
from ..view.project_creator import DataCreator
from ..view.project_loader import ProjectLoader
from ..view.setting import Setting
from .window_basics import SideMenuBarWindow
from ...libs.config import cfg
from qfluentwidgets import SystemThemeListener, isDarkTheme
from PyQt6.QtGui import QIcon

class StartWindow(SideMenuBarWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        data_selector = DataCreator(parent=self,parent_window=self)
        data_selector.setObjectName("data_selector")
        self.addSubInterface(
            data_selector,
            icon=Icon.NEWPROJECT,
            text=self.tr("New Project"),
            isTransparent=True
        )
        project_loader = ProjectLoader(parent=self,parent_window=self)
        project_loader.setObjectName("project_loader")
        self.addSubInterface(
            project_loader,
            icon=Icon.OPEN,
            text=self.tr("Load Project"),
            isTransparent=True
        )
        setting_view = Setting(parent=self)
        setting_view.setObjectName("setting_view")
        self.navigationInterface.addSeparator(position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(
            setting_view,
            icon=FluentIcon.SETTING,
            text=self.tr("Setting"),
            position=NavigationItemPosition.BOTTOM,
            isTransparent=True
        )
        self.themeListener.start()
        
"""
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
"""