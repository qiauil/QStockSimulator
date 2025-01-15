
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, PipsPager,PipsScrollButtonDisplayMode, FluentStyleSheet)

class PipsPagerNavigation(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.stacked_widget = QStackedWidget(self)
        self.pips_pager = PipsPager(self)
        self.pips_pager.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)
        self.pips_pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)
        self.pips_pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.stacked_widget)
        self.vBoxLayout.addWidget(self.pips_pager, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.currentChanged.connect(self.onCurrentIndexChanged)
        self.sub_interfaces = []
        FluentStyleSheet.FLUENT_WINDOW.apply(self.stacked_widget)

    
    def set_current_item(self, widget):
        self.stacked_widget.setCurrentWidget(widget)
        self.pips_pager.setCurrentIndex(self.stacked_widget.currentIndex())
        qrouter.setDefaultRouteKey(self.stacked_widget, widget.objectName())

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        #widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.stacked_widget.addWidget(widget)
        self.sub_interfaces.append(widget)
        self.pips_pager.setPageNumber(len(self.sub_interfaces))
        self.pips_pager.setVisibleNumber(len(self.sub_interfaces))
        if len(self.sub_interfaces) == 1:
            self.set_current_item(widget)
            self.pips_pager.setVisible(False)
        else:
            self.pips_pager.setVisible(True)

    def onCurrentIndexChanged(self, index):
        widget = self.stacked_widget.widget(index)
        self.pips_pager.setCurrentIndex(index)
        qrouter.push(self.stacked_widget, widget.objectName())

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication,QWidget,QVBoxLayout
    app = QApplication(sys.argv)
    widget = PipsPagerNavigation()
    widget.addSubInterface(QLabel("label1"), "widget1", "Widget1")
    #widget.addSubInterface(QLabel("label2"), "widget2", "Widget2")
    #widget.addSubInterface(QLabel("label3"), "widget3", "Widget3")
    widget.show()
    sys.exit(app.exec())