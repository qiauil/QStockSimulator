from qfluentwidgets import FluentIcon,NavigationItemPosition
from ...libs.style import Icon
from ...apps.project_creator import ProjectCreator
from ...apps.project_loader import ProjectLoader
from ...apps.setting import Setting
from ...gui.window import SideMenuBarWindow

class StartUpWindow(SideMenuBarWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        data_selector = ProjectCreator(parent=self,parent_window=self)
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
