from ...gui.widget.scroller_settings import ScrollerSettings
from ...libs.config import cfg
from qfluentwidgets import (OptionsSettingCard, CustomColorSettingCard,
                            setTheme, setThemeColor,FluentIcon)
from ...gui.window import DefaultWindow

class Setting(ScrollerSettings):

    def __init__(self, parent=None):
        super().__init__(self.tr("Setting"), False, parent=parent)

    def _init_widget(self):
        self.__init_personalization()

    def __init_personalization(self):
        personal_group = self.add_setting_card_group(self.tr('Personalization'))
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=personal_group
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            personal_group
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FluentIcon.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=personal_group
        )
        personal_group.addSettingCards(
            [self.themeCard, self.themeColorCard, self.zoomCard]
        )
        cfg.themeChanged.connect(setTheme)
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

class SettingWindow(DefaultWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Setting"))
        self.setMinimumSize(600, 700)
        self.setObjectName("setting_window")
        self.seeting=Setting(self)
        self.main_layout.addWidget(self.seeting)