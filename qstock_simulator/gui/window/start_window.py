from qfluentwidgets import FluentWindow, BodyLabel, FluentIcon,NavigationItemPosition
from ...libs.style import Icon
from ..view.project_creator import DataCreator
from ..view.project_loader import ProjectLoader
from .window_basics import ProgressiveMixin

class StartWindow(FluentWindow,ProgressiveMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(650, 650)
        self.setResizeEnabled(False)
        self.titleBar.maxBtn.hide()
        self.navigationInterface.setReturnButtonVisible(False)
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setAcrylicEnabled(True)

        data_selector = DataCreator(parent=self,parent_window=self)
        data_selector.setObjectName("data_selector")
        self.addSubInterface(
            data_selector,
            icon=Icon.NEWPROJECT,
            text="New Project",
            isTransparent=True
        )
        project_loader = ProjectLoader(parent=self,parent_window=self)
        project_loader.setObjectName("project_loader")
        self.addSubInterface(
            project_loader,
            icon=Icon.OPEN,
            text="Load Project",
            isTransparent=True
        )
        label_3=BodyLabel(
            "Welcome to Stock Simulator",
            parent=self
        )
        label_3.setObjectName("title3")
        self.navigationInterface.addSeparator(position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(
            label_3,
            icon=FluentIcon.SETTING,
            text="Setting",
            position=NavigationItemPosition.BOTTOM,
            isTransparent=True
        )
"""
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
"""