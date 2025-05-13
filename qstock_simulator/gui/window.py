from .widget.progress_message_box import ProgressMessageBox
from ..libs.utils import FunctionThread
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets import (
    isDarkTheme,
    qconfig,
    FluentTitleBar,
    TransparentToolButton,
    FluentIcon,
    RoundMenu,
    MenuAnimationType,
    Action,
    setTheme,
    Theme,
    CheckableMenu,
    MenuIndicatorType,
    SplashScreen,
    SystemThemeListener,
    FluentWindow
)
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget
from typing import Literal
from ..libs.config import cfg
from PyQt6.QtCore import QTimer
import sys


class SplashWindow(BackgroundAnimationWidget, FramelessWindow):

    def __init__(self, icon: QIcon, icon_size: int = 128, parent=None):
        super().__init__(parent=parent)
        self.titleBar.hide()
        self.splash_screen = SplashScreen(icon, parent=self)
        self.splash_screen.setIconSize(QSize(icon_size, icon_size))
        self.splash_screen.titleBar.hide()
        self.splash_screen.raise_()
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

class DefaultWindow(BackgroundAnimationWidget, FramelessWindow):
    def __init__(
        self,
        parent=None,
        main_lyout_direction: Literal["horizontal", "vertical"] = "horizontal",
    ):
        self._isMicaEnabled = False
        super().__init__(parent=parent)
        self.themeListener = SystemThemeListener(self)
        self.title_bar = FluentTitleBar(self)
        self.title_bar.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.setTitleBar(self.title_bar)
        self.setWindowTitle("QStock Simulator")
        self.setWindowIcon(QIcon("qstock_simulator/resources/pics/logo.png"))
        if main_lyout_direction == "horizontal":
            self.main_layout = QHBoxLayout(self)
        else:
            self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 48, 16, 16)

        # enable mica effect on win11
        self.setMicaEffectEnabled(True)

        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)
        self.themeListener.start()

    def _normalBackgroundColor(self):
        if not self.isMicaEffectEnabled():
            return QColor(32, 32, 32) if isDarkTheme() else QColor(243, 243, 243)

        return QColor(0, 0, 0, 0)

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

    def setMicaEffectEnabled(self, isEnabled: bool):
        """set whether the mica effect is enabled, only available on Win11"""
        if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

class TitleMenuWindow(DefaultWindow):
    def __init__(
        self,
        parent=None,
        main_lyout_direction: Literal["horizontal", "vertical"] = "horizontal",
        change_theme_action: bool = True,
    ):
        super().__init__(parent, main_lyout_direction)
        self.menu_button = TransparentToolButton(parent=self)
        self.menu_button.setIcon(FluentIcon.MENU)
        self.menu_button.setFixedSize(24, 24)
        self.title_bar.hBoxLayout.insertWidget(
            0,
            self.menu_button,
            0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        self.title_bar.hBoxLayout.insertSpacing(1, 12)
        self.menu = RoundMenu(parent=self)
        self.menu_button.clicked.connect(
            lambda: self.menu.exec(
                self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()),
                aniType=MenuAnimationType.FADE_IN_DROP_DOWN,
            )
        )
        if change_theme_action:
            auto_action = Action("Auto")
            auto_action.setIcon(FluentIcon.CONSTRACT)

            def auto_action_triggered():
                setTheme(Theme.AUTO)
                auto_action.setChecked(True)

            auto_action.triggered.connect(auto_action_triggered)
            light_action = Action("Light")
            light_action.setIcon(FluentIcon.BRIGHTNESS)

            def light_action_triggered():
                setTheme(Theme.LIGHT)
                auto_action.setChecked(False)

            light_action.triggered.connect(light_action_triggered)
            dark_action = Action("Dark")
            dark_action.setIcon(FluentIcon.QUIET_HOURS)

            def dark_action_triggered():
                setTheme(Theme.DARK)
                auto_action.setChecked(False)

            dark_action.triggered.connect(dark_action_triggered)
            change_theme_menu = CheckableMenu(
                "Theme", indicatorType=MenuIndicatorType.RADIO
            )
            change_theme_menu.addAction(light_action)
            change_theme_menu.addAction(dark_action)
            change_theme_menu.addAction(auto_action)
            change_theme_menu.setIcon(FluentIcon.PALETTE)
            self.menu.addMenu(change_theme_menu)
            auto_action.setCheckable(True)
            dark_action.setCheckable(True)
            light_action.setCheckable(True)
            auto_action.setChecked(True)

class ProgressiveMixin:

    def progressive_run(
        self, func, message: str = "Loading...", additional_func=None, **kwargs
    ):
        function_thread = FunctionThread(func, **kwargs)
        if additional_func is not None:

            def temp_func():
                additional_func()
                self.close_progress_message()

            function_thread.sigFunctionFinished.connect(temp_func)
        else:
            function_thread.sigFunctionFinished.connect(self.close_progress_message)
        function_thread.start()
        self.show_progress_message(message)

    def show_progress_message(self, message: str = "Loading..."):
        self.progress_message_box = ProgressMessageBox(self)
        self.progress_message_box.set_content(message)
        self.progress_message_box.exec()

    def close_progress_message(self):
        if self.progress_message_box is not None:
            self.progress_message_box.reject()
            self.progress_message_box = None

    def update_progress_message(self, message: str):
        self.progress_message_box.set_content(message)

class ProgressiveWindow(DefaultWindow, ProgressiveMixin):

    def __init__(self, parent=None,
                 main_lyout_direction: Literal["horizontal", "vertical"] = "horizontal"):
        super().__init__(parent, main_lyout_direction)

class SideMenuBarWindow(FluentWindow,ProgressiveMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("QStock Simulator"))
        self.setWindowIcon(QIcon("qstock_simulator/resources/pics/logo.png"))
        self.themeListener = SystemThemeListener(self)
        self.setFixedSize(650, 650)
        self.setResizeEnabled(False)
        self.titleBar.maxBtn.hide()
        self.navigationInterface.setReturnButtonVisible(False)
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setAcrylicEnabled(True)

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # retry
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = DefaultWindow()
    window.show()
    sys.exit(app.exec())
