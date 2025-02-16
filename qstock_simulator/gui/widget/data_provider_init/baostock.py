from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import CalendarPicker, BodyLabel, FluentIcon
from PyQt6.QtCore import Qt
from ..cards import TransparentWidgetCard

class BaoStockProviderInitGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        start_date_card = TransparentWidgetCard(
            FluentIcon.CALENDAR,
            "Start Date",
            "Search avaliable stock data from this date",
            parent=parent
        )
        self.start_date_picker = CalendarPicker(parent=start_date_card)
        start_date_card.add_widget(self.start_date_picker)
        self.start_date_picker.setDate(QDate(2010, 1, 1))
        self.start_date_picker.setDateFormat('yyyy-M-d')

        end_date_card = TransparentWidgetCard(
            FluentIcon.CALENDAR,
            "End Date",
            "Search avaliable stock data until this date",
            parent=parent
        )
        self.end_date_picker = CalendarPicker(parent=end_date_card)
        end_date_card.add_widget(self.end_date_picker)
        self.end_date_picker.setDate(QDate.currentDate())
        self.end_date_picker.setDateFormat('yyyy-M-d')

        self.main_layout.addWidget(start_date_card)
        self.main_layout.addWidget(end_date_card)
    
    def get_start_date(self):
        return self.start_date_picker.date.toString('yyyy-MM-dd')
    
    def get_end_date(self):
        return self.end_date_picker.date.toString('yyyy-MM-dd')