from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import CalendarPicker, BodyLabel

class BaoStockProviderInitGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        start_date_layout = QHBoxLayout()
        self.start_date_label = BodyLabel("Start Date:")
        self.start_date_picker = CalendarPicker()
        self.start_date_picker.setDate(QDate(2010, 1, 1))
        self.start_date_picker.setDateFormat('yyyy-M-d')
        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_picker)
        self.main_layout.addLayout(start_date_layout)

        end_date_layout = QHBoxLayout()
        self.end_date_label = BodyLabel("End Date:")
        self.end_date_picker = CalendarPicker()
        self.end_date_picker.setDate(QDate.currentDate())
        self.end_date_picker.setDateFormat('yyyy-M-d')
        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_picker)
        self.main_layout.addLayout(end_date_layout)
    
    def get_start_date(self):
        return self.start_date_picker.date.toString('yyyy-MM-dd')
    
    def get_end_date(self):
        return self.end_date_picker.date.toString('yyyy-MM-dd')