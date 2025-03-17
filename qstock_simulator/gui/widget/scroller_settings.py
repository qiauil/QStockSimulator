from qfluentwidgets import (
    PushButton,
    PrimaryPushButton,
    InfoBar,
    InfoBarPosition,
    ScrollArea,
    TitleLabel,
    SettingCardGroup,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


class ScrollerSettings(QWidget):

    def __init__(self, 
                 title:str,
                 show_control:bool=True,
                 next_button_text:str="Next",
                 back_button_text:str="Back",
                 show_back_button:bool=True,
                 parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10,0,0,0)
        self.title_label = TitleLabel(title, parent=self)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addSpacing(10)

        self._scroller=ScrollArea(parent=parent)
        self._scroller.setStyleSheet("background:transparent;border: none;")
        self._scroller_widget = QWidget(parent=self)
        self.content_layout = QVBoxLayout(self._scroller_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0,0,15,0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self._scroller)

        self.control_layout = QHBoxLayout()
        self.back_button = PushButton(back_button_text, parent=self)
        self.back_button.setMaximumWidth(100)
        self.next_button = PrimaryPushButton(next_button_text, parent=self)
        self.next_button.setMaximumWidth(100)
        self.next_button.setFocus()
        self.control_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.control_layout.addSpacing(50)
        self.control_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.control_layout.setContentsMargins(0,0,15,0)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addSpacing(10)

        if not show_control:
            self.back_button.hide()
            self.next_button.hide()
        if not show_back_button:
            self.back_button.hide()

        self._init_widget()
        self._enable_scroll()

    def change_title(self,title:str):
        self.title_label.setText(title)

    def _init_widget(self):
        raise NotImplementedError("This method should be implemented in subclass")

    def _enable_scroll(self):
        "scroll is only avaliable when all the wigets are added"
        self._scroller.setWidget(self._scroller_widget)
        self._scroller.setWidgetResizable(True)

    @property
    def next_clicked(self):
        return self.next_button.clicked
    
    @property
    def back_clicked(self):
        return self.back_button.clicked
    
    def add_setting_card_group(self,title:str):
        card_group = SettingCardGroup(
            title,
            parent=self._scroller_widget)
        self.content_layout.addWidget(card_group, alignment=Qt.AlignmentFlag.AlignTop)
        self.content_layout.addSpacing(20)
        return card_group
    
    def show_error_info(self,
                        title:str,
                        content:str,
                        ):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self.parent()
        )