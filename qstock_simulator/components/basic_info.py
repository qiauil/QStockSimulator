from ..gui.widget.price_volume_plotter import DWMPriceVolumeInfoPlotter
from ..libs.data import DataHandler
from ..libs.style import make_style
from qstock_plotter.libs.data_handler import TradeData
import pandas as pd
import pyqtgraph as pg
from pyqtgraph import PlotCurveItem
from qfluentwidgets import Action, FluentIcon


class BasicInfoComponent:

    def __init__(self, widget_parent=None, **kwargs):
        self.widget = DWMPriceVolumeInfoPlotter(widget_parent)
        self.day_data: TradeData = None
        self.week_data: TradeData = None
        self.month_data: TradeData = None
        self._day_start_index = 0
        self._day_end_index = 0
        self._week_start_index = 0
        self._week_end_index = 0
        self._month_start_index = 0
        self._month_end_index = 0
        self._first_initilized = True
        if "style" in kwargs:
            self.style = kwargs["style"]
        else:
            self.style = make_style()
        # initialize menus
        self.hide_info_action = Action("Stock info bar", parent=widget_parent)
        self.hide_info_action.setIcon(FluentIcon.VIEW)
        def hide_info_action_triggered():
            if self.widget.day_plotter.info_bar.isVisible():
                self.widget.set_info_bar_visible(False)
                self.hide_info_action.setIcon(FluentIcon.HIDE)
            else:
                self.widget.set_info_bar_visible(True)
                self.hide_info_action.setIcon(FluentIcon.VIEW)
        self.hide_info_action.triggered.connect(hide_info_action_triggered)
        self.hide_volume_action = Action("Volume plot", parent=widget_parent)
        self.hide_volume_action.setIcon(FluentIcon.VIEW)
        def hide_volume_action_triggered():
            if self.widget.day_plotter.volume_plotter.isVisible():
                self.widget.set_volume_plot_visible(False)
                self.hide_volume_action.setIcon(FluentIcon.VIEW)
            else:
                self.widget.set_volume_plot_visible(True)
                self.hide_volume_action.setIcon(FluentIcon.HIDE)
        self.hide_volume_action.triggered.connect(hide_volume_action_triggered)
        """
        self.hide_price_action = Action("Price plot", parent=widget_parent)
        self.hide_price_action.setIcon(FluentIcon.VIEW)
        def hide_price_action_triggered():
            if self.widget.day_plotter.price_plotter.isVisible():
                self.widget.set_price_plot_visible(False)
                self.hide_price_action.setIcon(FluentIcon.VIEW)
            else:
                self.widget.set_price_plot_visible(True)
                self.hide_price_action.setIcon(FluentIcon.HIDE)
        self.hide_price_action.triggered.connect(hide_price_action_triggered)
        """
        if hasattr(widget_parent, "menu"):
            widget_parent.menu.insertAction(widget_parent.menu.actions()[0], self.hide_info_action)
            widget_parent.menu.insertAction(widget_parent.menu.actions()[0], self.hide_volume_action)
            #widget_parent.menu.insertAction(widget_parent.menu.actions()[0], self.hide_price_action)

    def initialze(
        self, data_handler: DataHandler, start_index: int, current_index: int
    ):
        self._day_start_index = start_index
        self._day_end_index = current_index

        self.day_data = data_handler.day_data
        self.week_data = data_handler.week_data
        self.month_data = data_handler.month_data

        self.widget.add_data_handler(data_handler)
        if self._first_initilized:
            self._avoid_out_of_range()

        start_day = pd.to_datetime(self.day_data.prices.x_ticks[start_index])
        end_day = pd.to_datetime(self.day_data.prices.x_ticks[current_index])

        def find_index(data):
            start_index = 0
            end_index = 0
            find_start = False
            for i in range(len(data.prices)):
                if (
                    not find_start
                    and pd.to_datetime(data.prices.x_ticks[i]) >= start_day
                ):
                    start_index = i
                    find_start = True
                if pd.to_datetime(data.prices.x_ticks[i]) > end_day:
                    end_index = i - 1
                    break
            end_index = max(end_index, 0)
            return start_index, end_index

        self._week_start_index, self._week_end_index = find_index(self.week_data)
        self._month_start_index, self._month_end_index = find_index(self.month_data)

        self._move_day_view()
        self._move_week_view()
        self._move_month_view()

        if self._first_initilized:
            self.hide_volume_action.setIcon(FluentIcon.HIDE)
            for plotter in [self.widget.day_plotter, self.widget.week_plotter, self.widget.month_plotter]:
                plotter.volume_card.hide()

        self._first_initilized = False

    def _avoid_out_of_range(self):
        day_lambda = lambda: self.widget.day_plotter.set_x_range(
            self._day_start_index - 0.5, self._day_end_index + 0.5
        )
        self.widget.day_plotter.price_plotter.main_plotter.sigItemAdded.connect(
            day_lambda
        )
        self.widget.day_plotter.price_plotter.main_plotter.sigItemRemoved.connect(
            day_lambda
        )
        self.widget.day_plotter.volume_plotter.main_plotter.sigItemRemoved.connect(
            day_lambda
        )
        self.widget.day_plotter.volume_plotter.main_plotter.sigItemAdded.connect(
            day_lambda
        )
        week_lambda = lambda: self.widget.week_plotter.set_x_range(
            self._week_start_index - 0.5, self._week_end_index + 0.5
        )
        self.widget.week_plotter.price_plotter.main_plotter.sigItemAdded.connect(
            week_lambda
        )
        self.widget.week_plotter.price_plotter.main_plotter.sigItemRemoved.connect(
            week_lambda
        )
        self.widget.week_plotter.volume_plotter.main_plotter.sigItemRemoved.connect(
            week_lambda
        )
        self.widget.week_plotter.volume_plotter.main_plotter.sigItemAdded.connect(
            week_lambda
        )
        month_lambda = lambda: self.widget.month_plotter.set_x_range(
            self._month_start_index - 0.5, self._month_end_index + 0.5
        )
        self.widget.month_plotter.price_plotter.main_plotter.sigItemAdded.connect(
            month_lambda
        )
        self.widget.month_plotter.price_plotter.main_plotter.sigItemRemoved.connect(
            month_lambda
        )
        self.widget.month_plotter.volume_plotter.main_plotter.sigItemRemoved.connect(
            month_lambda
        )
        self.widget.month_plotter.volume_plotter.main_plotter.sigItemAdded.connect(
            month_lambda
        )

    def on_move_next_day(self):
        if self._day_end_index < len(self.day_data.prices):
            self._day_end_index += 1
            self._move_day_view()
            current_day = pd.to_datetime(
                self.day_data.prices.x_ticks[self._day_end_index]
            )
            if self.week_data is not None:
                if self._week_end_index + 1 < len(self.week_data.prices):
                    next_week_day = pd.to_datetime(
                        self.week_data.prices.x_ticks[self._week_end_index + 1]
                    )
                    if next_week_day <= current_day:
                        self._week_end_index += 1
                        self._move_week_view()
            if self.month_data is not None:
                if self._month_end_index + 1 < len(self.month_data.prices):
                    next_month_day = pd.to_datetime(
                        self.month_data.prices.x_ticks[self._month_end_index + 1]
                    )
                    if next_month_day <= current_day:
                        self._month_end_index += 1
                        self._move_month_view()
        else:
            raise ValueError("End of day data")

    def _move_day_view(self):
        self.widget.day_plotter.set_x_range(
            self._day_start_index - 0.5, self._day_end_index + 0.5
        )
        self.widget.day_plotter.move_to_end()
        self.widget.day_plotter.show_info(self._day_end_index)

    def _move_week_view(self):
        self.widget.week_plotter.set_x_range(
            self._week_start_index - 0.5, self._week_end_index + 0.5
        )
        self.widget.week_plotter.move_to_end()
        self.widget.week_plotter.show_info(self._week_end_index)

    def _move_month_view(self):
        self.widget.month_plotter.set_x_range(
            self._month_start_index - 0.5, self._month_end_index + 0.5
        )
        self.widget.month_plotter.move_to_end()
        self.widget.month_plotter.show_info(self._month_end_index)

    def add_buy_line(self, index: int):
        self.widget.day_plotter.price_plotter.main_plotter.add_item(
            PlotCurveItem(
                x=[index, index],
                y=[
                    self.widget.day_plotter.price_plotter.main_plotter.y_start,
                    self.widget.day_plotter.price_plotter.main_plotter.y_end,
                ],
                pen=pg.mkPen(
                    color=self.style["buy_line_color"],
                    width=self.style["buy_sell_line_width"],
                ),
            )
        )

    def add_sell_line(self, index: int):
        self.widget.day_plotter.price_plotter.main_plotter.add_item(
            PlotCurveItem(
                x=[index, index],
                y=[
                    self.widget.day_plotter.price_plotter.main_plotter.y_start,
                    self.widget.day_plotter.price_plotter.main_plotter.y_end,
                ],
                pen=pg.mkPen(
                    color=self.style["sell_line_color"],
                    width=self.style["buy_sell_line_width"],
                ),
            )
        )
