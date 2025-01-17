from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from qfluentwidgets import CalendarPicker, BodyLabel, DoubleSpinBox


class ChineseStockMarketTradeCoreInitGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        configs=[
            ("commission rate:",3.0,"‱"),
            ("min commission:",5.0,"RMB"),
            ("tax rate:",0.1,"‱"),
            ("transfer fee rate:",0.1,"‱"),
            ("trade fee rate:",0.341,"‱")
        ]
        self.spinboxs = []
        for config in configs:
            layout, spin_box = self._create_spin_box(*config)
            self.main_layout.addLayout(layout)
            self.spinboxs.append(spin_box)

    def _create_spin_box(self, 
                         description:str,
                         default_value:float,
                         postfix:str="",
                         ):
        layout = QHBoxLayout()
        label = BodyLabel(description)
        label.setMinimumWidth(100)
        spin_box = DoubleSpinBox()
        spin_box.setMinimum(0.0)
        spin_box.setValue(default_value)
        spin_box.setFixedWidth(150)
        postfix_label = BodyLabel(postfix)
        layout.addWidget(label)
        layout.addWidget(spin_box)
        layout.addWidget(postfix_label)
        return layout, spin_box
    
    def current_values(self) -> dict:
        return {
            "commission_rate":self.spinboxs[0].value(),
            "min_commission":self.spinboxs[1].value(),
            "tax_rate":self.spinboxs[2].value(),
            "transfer_fee_rate":self.spinboxs[3].value(),
            "trade_fee_rate":self.spinboxs[4].value()
        }

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ChineseStockMarketTradeCoreInitGUI()
    window.show()
    sys.exit(app.exec())