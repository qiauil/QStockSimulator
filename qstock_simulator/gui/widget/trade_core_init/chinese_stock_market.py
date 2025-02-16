from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from qfluentwidgets import CalendarPicker, BodyLabel, DoubleSpinBox, FluentIcon
from ....libs.style import Icon
from ..cards import TransparentWidgetCard


class ChineseStockMarketTradeCoreInitGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)
        configs=[
            ("Commission rate:",3.0,"Unit: ten-thousandth",Icon.MONEY),
            ("Min commission fee:",5.0,"Unit: RMB",Icon.MONEY),
            ("Tax rate:",0.1,"Unit: ten-thousandth",Icon.MONEY),
            ("Transfer fee rate:",0.1,"Unit: ten-thousandth",Icon.MONEY),
            ("Trade fee rate:",0.341,"Unit: ten-thousandth",Icon.MONEY)
        ]
        self.spinboxs = []
        for config in configs:
            card, spin_box = self._create_spin_box(*config)
            self.main_layout.addWidget(card)
            self.spinboxs.append(spin_box)

    def _create_spin_box(self, 
                         title:str,
                         default_value:float,
                         content:str="",
                         icon:FluentIcon=FluentIcon.MORE) -> tuple[TransparentWidgetCard, DoubleSpinBox]:
        card = TransparentWidgetCard(
            title=title,
            content=content,
            icon=icon,
            parent=self
        )
        spin_box = DoubleSpinBox(parent=card)
        spin_box.setMinimum(0.0)
        spin_box.setValue(default_value)
        spin_box.setFixedWidth(150)
        card.add_widget(spin_box)
        return card, spin_box
    
    def current_values(self) -> dict:
        return {
            "commission_rate":self.spinboxs[0].value()*0.0001,
            "min_commission":self.spinboxs[1].value(),
            "tax_rate":self.spinboxs[2].value()*0.0001,
            "transfer_fee_rate":self.spinboxs[3].value()*0.0001,
            "trade_fee_rate":self.spinboxs[4].value()*0.0001
        }

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ChineseStockMarketTradeCoreInitGUI()
    window.show()
    sys.exit(app.exec())