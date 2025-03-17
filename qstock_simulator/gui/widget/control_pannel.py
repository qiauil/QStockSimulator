from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QColor
from pyqtgraph import PlotCurveItem
import pyqtgraph as pg
import numpy as np
from qfluentwidgets import (
    CommandBar,
    setFont,
    FluentIcon,
    Action,
    SimpleCardWidget,
    BodyLabel,
    SpinBox,
    ProgressRing,
)
from qstock_plotter.widgets.q_plot_widget import QPlotWidget
from qstock_plotter.widgets.colorful_toggle_button import ColorfulToggleButton
from typing import Optional
from ...libs.style import make_style
from qstock_plotter.libs.helpers import ConfigurationsHandler
from typing import Sequence


class TradeInfoLineItem(PlotCurveItem):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def get_local_plot_range(self, start: float, end: float):
        """
        Returns the minimum and maximum values of the average line within the specified range.

        Args:
            start (float): The start value of the range.
            end (float): The end value of the range.

        Returns:
            tuple: A tuple containing the minimum and maximum values of the average line within the range.
                   If there are no data points within the range, returns None.
        """
        _, ys = self.getData()
        ys = ys[max(int(start), 0) : min(int(end), len(ys))]
        if len(ys) > 0:
            return np.min(ys), np.max(ys)
        else:
            return None


class ControlCommandBar(CommandBar):

    def __init__(self, parent=None):
        """
        Initialize the DrawLineCommandBar.

        Args:
            parent: The parent widget. Defaults to None.
            show_text_editor: Flag to show the text editor. Defaults to True.
        """
        super().__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # self.buy_amount_box = LineEdit(self)
        # self.buy_amount_box.setClearButtonEnabled(True)
        # self.buy_amount_box.setPlaceholderText('Buy in ammount')
        # self.buy_amount_box.setMinimumWidth(200)
        self.buy_amount_box = SpinBox(self)
        self.buy_amount_box.setMinimum(0)
        self.buy_amount_box.setMaximum(100000)
        self.buy_amount_box.setValue(100)
        self.addWidget(self.buy_amount_box)
        self.buy_money_label = BodyLabel("0", parent=self)
        self.addWidget(self.buy_money_label)
        self.buy_action = Action(FluentIcon.ADD, self.tr("Buy"), parent=self)
        self.addAction(self.buy_action)
        self.addSeparator()

        # self.sell_amount_box = LineEdit(self)
        # self.sell_amount_box.setClearButtonEnabled(True)
        # self.sell_amount_box.setPlaceholderText('Sell out ammount')
        # self.sell_amount_box.setMinimumWidth(200)
        self.sell_amount_box = SpinBox(self)
        self.sell_amount_box.setMinimum(0)
        self.sell_amount_box.setMaximum(100000)
        self.sell_amount_box.setValue(100)
        self.addWidget(self.sell_amount_box)
        self.sell_action = Action(FluentIcon.REMOVE, self.tr("Sell"), parent=self)
        self.addAction(self.sell_action)
        self.addSeparator()

        self.next_day_action = Action(FluentIcon.CHEVRON_RIGHT, self.tr("Next"), parent=self)
        # self.next_day_action = Action('Next', parent=self)
        self.addAction(self.next_day_action)
        """
        self.progress_ring = ProgressRing(parent=self)
        self.progress_ring.setMaximum(200)
        self.progress_ring.setValue(50)
        self.progress_ring.setFixedSize(24,24)
        self.addWidget(self.progress_ring)
        """

        self.setMinimumWidth(650)

    def set_enabled(self, enabled: bool):
        """
        Set the enabled state of the actions.

        Args:
            enabled: The enabled state.
        """
        for action_i in [self.buy_action, self.sell_action, self.next_day_action]:
            action_i.setEnabled(enabled)
        self.ammount_edit.setEnabled(enabled)


class TradeInfoTabel(QWidget):

    def __init__(self, parent=None, style: Optional[ConfigurationsHandler] = None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        self.setLayout(self.main_layout)
        self.color_button_layout = QVBoxLayout()
        self.title_layout = QVBoxLayout()
        self.value_layout = QVBoxLayout()
        self.color_button_layout.setSpacing(2)
        self.title_layout.setSpacing(2)
        self.value_layout.setSpacing(2)
        self.main_layout.addLayout(self.color_button_layout)
        self.main_layout.addLayout(self.title_layout)
        separate_label = BodyLabel(parent=self)
        separate_label.setFixedSize(24, 1)
        self.main_layout.addWidget(separate_label)
        self.main_layout.addLayout(self.value_layout)
        self.initial_amount_label = self._add_info(self.tr("Initial money:"), self.tr("0"))
        self.label_height = self.initial_amount_label.height()

        def get_temp_label():
            temp_label = BodyLabel(parent=self)
            temp_label.setFixedSize(1, self.label_height)
            return temp_label

        def create_button_layout():
            button_layout = QHBoxLayout()
            button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            button_layout.addWidget(get_temp_label())
            return button_layout

        self.initial_amount_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.initial_amount_button_layout)

        self.available_amount_label = self._add_info(self.tr("Avaliable money:"), self.tr("0"))
        self.avaliable_amount_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.avaliable_amount_button_layout)

        self.invested_amount_label = self._add_info(self.tr("Invested money:"), self.tr("0"))
        self.invested_amount_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.invested_amount_button_layout)

        self.invested_stock_label = self._add_info(self.tr("Invested stock:"), self.tr("0"))
        self.invested_stock_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.invested_stock_button_layout)

        self.current_amount_label = self._add_info(self.tr("Current money:"), self.tr("0"))
        self.current_money_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.current_money_button_layout)

        self.cost_label = self._add_info(self.tr("Cost:"), self.tr("0"))
        self.cost_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.cost_button_layout)

        self.profit_label = self._add_info(self.tr("Profit:"), self.tr("0"))
        self.profit_button_layout = create_button_layout()
        self.color_button_layout.addLayout(self.profit_button_layout)

        self.plot_style = style if style is not None else make_style()

    def _add_info(self, title: str, value: str):
        title_label = BodyLabel(title, parent=self)
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_label = BodyLabel(value, parent=self)
        value_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_layout.addWidget(title_label)
        self.value_layout.addWidget(value_label)
        return value_label

    def update_info(
        self,
        initial: Optional[float] = None,
        avaliable: Optional[float] = None,
        invested_money: Optional[float] = None,
        invested_stock: Optional[int] = None,
        cost: Optional[float] = None,
    ):
        if initial is not None:
            self.initial_amount_label.setText(f"{initial:.2f}")
        if avaliable is not None:
            self.available_amount_label.setText(f"{avaliable:.2f}")
        if invested_money is not None:
            self.invested_amount_label.setText(f"{invested_money:.2f}")
        if invested_stock is not None:
            self.invested_stock_label.setText(str(invested_stock))
        if cost is not None:
            self.cost_label.setText(f"{cost:.2f}")
        avaliable = float(self.available_amount_label.text())
        invested = float(self.invested_amount_label.text())
        initial = float(self.initial_amount_label.text())
        current = avaliable + invested
        self.current_amount_label.setText(str(current))
        profit = current - initial
        if profit == 0:
            self.profit_label.setTextColor(QColor(0, 0, 0),QColor(255, 255, 255))
            self.profit_label.setText("0(0%)")
        elif profit > 0:
            self.profit_label.setTextColor(self.plot_style.positive_color,self.plot_style.positive_color)
            self.profit_label.setText(f"+{profit:.2f}({profit/initial*100:.2f}%)")
        else:
            self.profit_label.setTextColor(self.plot_style.negative_color,self.plot_style.negative_color)
            self.profit_label.setText(f"-{profit:.2f}({profit/initial*100:.2f}%)")


class ControlPannel(QWidget):

    def __init__(self, parent=None, style: Optional[ConfigurationsHandler] = None):
        super().__init__(parent)
        style = style if style is not None else make_style()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        self.setLayout(self.main_layout)

        self.command_card = SimpleCardWidget(parent=self)
        self.command_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.command_card)
        self.command_card_layout = QHBoxLayout()
        self.command_card.setLayout(self.command_card_layout)
        self.control_command_bar = ControlCommandBar(self)
        self.command_card_layout.addWidget(self.control_command_bar)
        self.progress_layout = QHBoxLayout()
        self.progress_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.command_card_layout.addLayout(self.progress_layout)
        self.progress_label = BodyLabel("0/0", parent=self)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_label.setFixedSize(150, 20)
        self.progress_ring = ProgressRing(parent=self)
        self.progress_ring.setFixedSize(20, 20)
        self.progress_ring.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress_ring)

        self.info_plot_card = SimpleCardWidget(parent=self)
        self.info_plot_layout = QHBoxLayout()
        self.info_plot_layout.setSpacing(32)
        self.info_plot_card.setLayout(self.info_plot_layout)
        self.trade_info_table = TradeInfoTabel(parent=self, style=style)
        self.info_plot_layout.addWidget(self.trade_info_table)
        self.profit_plot = QPlotWidget(parent=self)
        # self.profit_plot.setMinimumHeight(5)
        self.info_plot_layout.addWidget(self.profit_plot)
        self.info_plot_card.setMaximumHeight(250)

        self.main_layout.addWidget(self.info_plot_card)
        self.main_layout.addWidget(self.command_card)

        self.lines = {
            "current": TradeInfoLineItem(
                pen=pg.mkPen(color=style.current_money_color, width=4)
            ),
            "invested": TradeInfoLineItem(
                pen=pg.mkPen(color=style.invested_money_color, width=4)
            ),
            "avaliable": TradeInfoLineItem(
                pen=pg.mkPen(color=style.avaliable_money_color, width=4)
            ),
        }
        self.profit_plot.add_item(self.lines["current"])
        current_toggle_button = ColorfulToggleButton(
            color=style.current_money_color, text="", parent=self
        )
        current_toggle_button.setChecked(True)
        current_toggle_button.setFixedSize(
            int(self.trade_info_table.label_height / 2),
            int(self.trade_info_table.label_height / 2),
        )

        def on_current_toggle_button_clicked():
            if current_toggle_button.isChecked():
                self.profit_plot.add_item(self.lines["current"])
            else:
                self.profit_plot.remove_item(self.lines["current"])

        current_toggle_button.clicked.connect(on_current_toggle_button_clicked)
        self.trade_info_table.current_money_button_layout.addWidget(
            current_toggle_button
        )
        self.profit_plot.add_item(self.lines["invested"])
        invested_toggle_button = ColorfulToggleButton(
            color=style.invested_money_color, text="", parent=self
        )
        invested_toggle_button.setChecked(True)
        invested_toggle_button.setFixedSize(
            int(self.trade_info_table.label_height / 2),
            int(self.trade_info_table.label_height / 2),
        )

        def on_invested_toggle_button_clicked():
            if invested_toggle_button.isChecked():
                self.profit_plot.add_item(self.lines["invested"])
            else:
                self.profit_plot.remove_item(self.lines["invested"])

        invested_toggle_button.clicked.connect(on_invested_toggle_button_clicked)
        self.trade_info_table.invested_amount_button_layout.addWidget(
            invested_toggle_button
        )
        self.profit_plot.add_item(self.lines["avaliable"])
        avaliable_toggle_button = ColorfulToggleButton(
            color=style.avaliable_money_color, text="", parent=self
        )
        avaliable_toggle_button.setChecked(True)
        avaliable_toggle_button.setFixedSize(
            int(self.trade_info_table.label_height / 2),
            int(self.trade_info_table.label_height / 2),
        )

        def on_avaliable_toggle_button_clicked():
            if avaliable_toggle_button.isChecked():
                self.profit_plot.add_item(self.lines["avaliable"])
            else:
                self.profit_plot.remove_item(self.lines["avaliable"])

        avaliable_toggle_button.clicked.connect(on_avaliable_toggle_button_clicked)
        self.trade_info_table.avaliable_amount_button_layout.addWidget(
            avaliable_toggle_button
        )

    def _update_line_data(self, line_name: str, y: float):
        xs, ys = self.lines[line_name].getData()
        if len(xs) == 0:
            xs = np.array([0])
            ys = np.array([y])
        else:
            xs = np.append(xs, xs[-1] + 1)
            ys = np.append(ys, y)
        self.lines[line_name].setData(xs, ys)
        self.profit_plot.refresh_bounding()

    def _set_line_data(self, line_name: str, x:Sequence[int], y: Sequence[float]):
        self.lines[line_name].setData(np.asarray(x), np.asarray(y))
        self.profit_plot.refresh_bounding()

    def set_plot_x_ticks(self, x_ticks):
        self.profit_plot.getAxis("bottom").set_tick_strings(x_ticks)

    def update_current_money_plot(self, y: float):
        self._update_line_data("current", y)
    
    def set_current_money_plot(self, x:Sequence[int], y: Sequence[float]):
        self._set_line_data("current", x, y)

    def update_invested_money_plot(self, y: float):
        self._update_line_data("invested", y)

    def set_invested_money_plot(self, x:Sequence[int], y: Sequence[float]):
        self._set_line_data("invested", x, y)

    def update_avaliable_money_plot(self, y: float):
        self._update_line_data("avaliable", y)

    def set_avaliable_money_plot(self, x:Sequence[int], y: Sequence[float]):
        self._set_line_data("avaliable", x, y)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)
    draw_line_command_bar = ControlPannel()
    layout.addWidget(draw_line_command_bar)
    window.show()
    sys.exit(app.exec())
