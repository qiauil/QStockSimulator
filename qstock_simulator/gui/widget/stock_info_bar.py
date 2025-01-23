from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from qfluentwidgets import SimpleCardWidget, PixmapLabel, BodyLabel, ImageLabel, FluentIcon
from qfluentwidgets.common.icon import toQIcon
from PyQt6.QtGui import QColor,QPixmap,QIcon
from PyQt6.QtCore import Qt
from typing import Optional

class StockInfoBar(QWidget):

    def __init__(self, parent = None,):
        super().__init__(parent)
        self.stock_info_card = SimpleCardWidget()
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.stock_info_card)
        self.card_layout = QHBoxLayout(self.stock_info_card)
        self.stock_info_card.setLayout(self.card_layout)
        self.card_layout.setSpacing(32)

        #self.colorful_state_label = PixmapLabel()
        #self.card_layout.addWidget(self.colorful_state_label)

        self.time_label = BodyLabel("2025-01-01")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.card_layout.addWidget(self.time_label)

        self.initial_value_label = self._creat_label_groups("Initial:")

        self.end_value_label, end_value_layout = self._creat_label_groups("End:", return_layout=True)
        self.end_value_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.price_change_label = BodyLabel("(+32, +0.32%)")
        self.price_change_label.setTextColor(QColor("green"),QColor("green"))
        self.price_change_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.price_change_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        end_value_layout.addWidget(self.price_change_label)

        self.price_change_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lowest_value_label = self._creat_label_groups("Lowest:")
        self.highest_value_label,highest_value_layout = self._creat_label_groups("Highest:",return_layout=True)
        self.highest_value_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.price_deviation_label = BodyLabel("(+72)")
        self.price_deviation_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        highest_value_layout.addWidget(self.price_deviation_label)


        self.volume_label = self._creat_label_groups("Volume:")

        self.stock_info_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #self.set_state_color(QColor("red"))
        self.set_stock_info("2025-01-01",100.0, 200.0, 300.0, 50.0, 1000.0)

    def _creat_label_groups(self, label_text: str, label_value: str = "0.0", return_layout=False) -> BodyLabel:
        layout = QHBoxLayout()
        layout.setSpacing(4)
        self.card_layout.addLayout(layout)
        title_label = BodyLabel(label_text)
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        value_label = BodyLabel(label_value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        if return_layout:
            return value_label,layout
        return value_label

    """
    def set_state_color(self, color: QColor):
        pixmap = QPixmap(16,16)
        pixmap.fill(color)
        self.colorful_state_label.setPixmap(pixmap)
    """
    def set_stock_info(self, 
                       time:Optional[str],
                       initial:Optional[float], 
                       end:Optional[float], 
                       highest:Optional[float], 
                       lowest:Optional[float], 
                       volume:Optional[float],
                       positive_color:Optional[QColor] = None,
                       negative_color:Optional[QColor] = None,
                       ):
        if time is not None:
            self.time_label.setText(time)
        if initial is not None:
            self.initial_value_label.setText(f"{initial:.2f}")
        if end is not None:
            self.end_value_label.setText(f"{end:.2f}")
        if highest is not None:
            self.highest_value_label.setText(f"{highest:.2f}")
        if lowest is not None:
            self.lowest_value_label.setText(f"{lowest:.2f}")
        if volume is not None:
            self.volume_label.setText(f"{volume:.2f}")
        positive_color= QColor("red") if positive_color is None else positive_color
        negative_color = QColor("green") if negative_color is None else negative_color
        initial=float(self.initial_value_label.text())
        end=float(self.end_value_label.text())
        if end > initial:
            self.price_change_label.setTextColor(positive_color,positive_color)
            self.price_change_label.setText(f"(+{end-initial:.2f}, +{100*(end-initial)/initial:.2f}%)")
        else:
            self.price_change_label.setTextColor(negative_color,negative_color)
            self.price_change_label.setText(f"(-{initial-end:.2f}, -{100*(initial-end)/initial:.2f}%)")
        highest = float(self.highest_value_label.text())
        lowest = float(self.lowest_value_label.text())
        self.price_deviation_label.setText(f"(+{highest-lowest:.2f})")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = StockInfoBar()
    window.show()
    sys.exit(app.exec())