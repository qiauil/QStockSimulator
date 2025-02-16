from qfluentwidgets import FluentWindow, BodyLabel, FluentIcon,NavigationItemPosition
from ...libs.style import Icon
from ..widget.data_selector import DataSelector
from .window_basics import ProgressiveMixin

class StartWindow(FluentWindow,ProgressiveMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(550, 650)
        self.setResizeEnabled(False)
        self.titleBar.maxBtn.hide()

        data_selector = DataSelector(parent=self,parent_window=self)
        data_selector.setObjectName("data_selector")
        self.addSubInterface(
            data_selector,
            icon=Icon.NEWPROJECT,
            text="New Project",
            isTransparent=True
        )
        label_2=BodyLabel(
            "Welcome to Stock Simulator",
            parent=self
        )
        label_2.setObjectName("title2")
        self.addSubInterface(
            label_2,
            icon=Icon.OPEN,
            text="Open",
        )
        label_3=BodyLabel(
            "Welcome to Stock Simulator",
            parent=self
        )
        label_3.setObjectName("title3")
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