from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase
from qfluentwidgets import (
    IndeterminateProgressRing,
    SimpleCardWidget,
    isDarkTheme,
    BodyLabel
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout


class BackgroundCardWidget(SimpleCardWidget):
    """Simple card widget"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def _normalBackgroundColor(self):
        return QColor(255, 255, 255, 16) if isDarkTheme() else QColor(255, 255, 255)


class ProgressMessageBox(MaskDialogBase):

    def __init__(self, 
                 parent,
                 show_content_label: bool = True,):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self.widget)
        self.card = BackgroundCardWidget(parent=self.widget)
        self.card.setFixedSize(200, 200)
        self.main_layout.addWidget(self.card)
        self.card_layout = QVBoxLayout(self.card)
        self.progress_ring = IndeterminateProgressRing(parent=self.widget)
        self.card_layout.addWidget(self.progress_ring,alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_label = BodyLabel(self.tr("Loading..."), parent=self.widget)
        self.card_layout.addWidget(self.content_label,alignment=Qt.AlignmentFlag.AlignCenter)
        if not show_content_label:
            self.content_label.hide()
        else:
            self.card_layout.setContentsMargins(0, 40, 0, 0)

    def set_content(self, content: str):
        self.content_label.setText(content)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QWidget
    from qfluentwidgets import PushButton

    class Demo(QWidget):
        def __init__(self):
            super().__init__()

            self.hBxoLayout = QHBoxLayout(self)
            self.button = PushButton("Show", self)

            self.resize(600, 600)
            self.hBxoLayout.addWidget(
                self.button,
                0,
            )
            self.button.clicked.connect(self.showDialog)

        def showDialog(self):
            w = ProgressMessageBox(self)
            w.exec()

    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())
