from qfluentwidgets import PushSettingCard, FluentIcon, SettingCard, FluentIconBase, ExpandSettingCard, LineEdit
from PyQt6.QtWidgets import QFileDialog, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from typing import Union,Sequence
from PyQt6.QtCore import pyqtSignal

class FolderSelectCard(PushSettingCard):

    sigFolderChanged = pyqtSignal(str)

    def __init__(self, button_text="Select", 
                 icon=FluentIcon.FOLDER, 
                 title="Project Folder", 
                 empty_folder_content="No folder selected", parent=None):
        super().__init__(            
            button_text,
            icon=icon,
            title=title,
            content=empty_folder_content,
            parent=parent,)
        self._current_folder = None
        self.clicked.connect(self.__on_select_button_clicked)
        self.empty_folder_content = empty_folder_content

    def __on_select_button_clicked(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder:
            return
        self.set_folder(folder)
        self.sigFolderChanged.emit(folder)
    
    def set_folder(self, folder):
        self._current_folder = folder
        if folder is None:
            folder=self.empty_folder_content
        self.setContent(folder)

    def sizeHint(self):
        return QSize(100, 70)
    @property
    def current_folder(self):
        return self._current_folder

class TransparentFolderSelectCard(FolderSelectCard):
    def __init__(self, button_text="Select", 
                 icon=FluentIcon.FOLDER, 
                 title="Project Folder", 
                 empty_folder_content="No folder selected", parent=None):
        super().__init__(button_text, icon, title, empty_folder_content, parent)
    
    def paintEvent(self, e):
        return None

class WidgetCard(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, 
                 icon: Union[str, QIcon, FluentIconBase], 
                 title, 
                 content=None,
                 widget:QWidget=None, 
                 parent=None):
        super().__init__(icon, title, content, parent)
        if widget is not None:
            self.add_widget(widget)
    
    def add_widget(self, widget:QWidget):
        self.hBoxLayout.addWidget(widget, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

class LineEditCard(WidgetCard):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], 
                 title, 
                 content=None,
                 text="",
                 parent=None):
        super().__init__(icon, title, content, None, parent)
        self.line_edit = LineEdit(self)
        self.line_edit.setText(text)
        self.line_edit.setFixedHeight(30)
        self.line_edit.setClearButtonEnabled(True)
        self.add_widget(self.line_edit)
    
    def text(self):
        return self.line_edit.text()
    
    def set_text(self, text):
        self.line_edit.setText(text)

class TransparentWidgetCard(WidgetCard):

    def __init__(self, icon, title, content=None, widget = None, parent=None):
        super().__init__(icon, title, content, widget, parent)

    def paintEvent(self, e):
        return None
    
class ExpandWidgetCard(ExpandSettingCard):
    
    def __init__(self, icon, title, content=None, widget = None, parent=None):
        super().__init__(icon, title, content, parent)
        if widget is not None:
            self.add_widget(widget)
    
    def add_widget(self, widget:QWidget):
        self.addWidget(widget)

    def add_content_widget(self, widget:Union[QWidget, Sequence[QWidget]]):
        if isinstance(widget, QWidget):
            widget = [widget]
        for w in widget:
            self.viewLayout.addWidget(w)
        self._adjustViewSize()