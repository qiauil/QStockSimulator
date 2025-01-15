from ..gui.window.trade_window import TradeWindow
from ..components.basic_info import BasicInfoComponent
from ..libs.trade_core import TradeCore, BuyState, SellState
from qstock_plotter.libs.data_handler import DataHandler
from typing import Optional


class MainTrade(TradeWindow):

    def __init__(
        self,
        data_handler: DataHandler,
        start_index: int,
        end_index: int,
        current_index: int,
        trade_core: TradeCore,
        start_trade_index: Optional[int] = None,
        parent=None,
    ):
        super().__init__(parent=parent)
        # initialze main data
        self.start_index = start_index
        self.end_index = end_index
        self.current_index = current_index
        self.start_trade_index = (
            start_trade_index if start_trade_index is not None else current_index
        )
        self.day_data = data_handler.day_data
        if self.end_index >= len(data_handler.day_data.prices):
            raise ValueError("End index is out of range")
        # initialize components
        self.basic_info_component = BasicInfoComponent(widget_parent=self)
        self.components = [
            self.basic_info_component,
        ]
        for component in self.components:
            if hasattr(component, "widget"):
                self.stock_info_navigation.addSubInterface(
                    component.widget,
                    component.__class__.__name__,
                    component.__class__.__name__,
                )
        for component in self.components:
            if hasattr(component, "initialze"):
                component.initialze(data_handler, start_index, current_index)
        # initialize widgets
        ticks = {}
        index = 0
        full_tick = self.day_data.prices.get_x_ticks()
        for i in range(start_index, end_index + 1):
            ticks[index] = full_tick[i]
            index += 1
        self.control_pannel.set_plot_x_ticks(ticks)
        self.control_pannel.progress_ring.setMaximum(
            self.end_index - self.start_trade_index
        )
        self.control_pannel.progress_ring.setValue(
            self.current_index - self.start_trade_index
        )
        self.control_pannel.progress_label.setText(
            f"{self.current_index-self.start_trade_index}/{self.end_index-self.start_trade_index}"
        )
        # set up trade core
        self.trade_core = trade_core
        t, initial, close, high, low = self.day_data.prices[self.current_index]
        self.trade_core.current_price = close
        self._update_trade_state()
        # connect signals
        self.control_pannel.control_command_bar.next_day_action.triggered.connect(
            self.on_move_next_day
        )
        self.control_pannel.control_command_bar.buy_action.triggered.connect(
            self.on_buy_stock
        )
        self.control_pannel.control_command_bar.sell_action.triggered.connect(
            self.on_sell_stock
        )
        self.control_pannel.control_command_bar.buy_amount_box.valueChanged.connect(
            self.on_buy_amount_changed
        )
        self.control_pannel.control_command_bar.sell_amount_box.valueChanged.connect(
            self.on_sell_amount_changed
        )
        # other settings
        if self.current_index == self.end_index:
            self.on_finish_simulation()

    def _update_trade_state(self):
        self.control_pannel.trade_info_table.update_info(
            initial=self.trade_core.initial_money,
            avaliable=self.trade_core.avaliable_money,
            invested_money=self.trade_core.invested_money,
            invested_stock=self.trade_core.invested_stock,
            cost=self.trade_core.handling_fee_total,
        )
        self.control_pannel.control_command_bar.buy_money_label.setText(
            f"={self.trade_core.current_price*self.control_pannel.control_command_bar.buy_amount_box.value():.2f}"
        )
        self.control_pannel.update_avaliable_money_plot(self.trade_core.avaliable_money)
        self.control_pannel.update_invested_money_plot(self.trade_core.invested_money)
        self.control_pannel.update_current_money_plot(
            self.trade_core.avaliable_money + self.trade_core.invested_money
        )
        self.control_pannel.profit_plot.full_range()

    def on_move_next_day(self):
        self.current_index += 1
        t, initial, close, high, low = self.day_data.prices[self.current_index]
        self.trade_core.move_to_next_day(close)
        self._update_trade_state()
        self.control_pannel.progress_ring.setValue(
            self.current_index - self.start_trade_index
        )
        self.control_pannel.progress_label.setText(
            f"{self.current_index-self.start_trade_index}/{self.end_index-self.start_trade_index}"
        )
        for component in self.components:
            if hasattr(component, "on_move_next_day"):
                component.on_move_next_day()
        if self.current_index == self.end_index:
            self.on_finish_simulation()

    def on_buy_stock(self):
        self.on_move_next_day()
        num_stock = self.control_pannel.control_command_bar.buy_amount_box.value()
        state, invested = self.trade_core.buy(num_stock)
        if state == BuyState.NOT_ENOUGH_MONEY:
            self.show_error_info(
                title="Not enough money",
                content="You don't have enough money to buy {} stocks".format(
                    num_stock
                ),
            )
        elif state == BuyState.NOT_ALLOWED_AMOUNT:
            self.show_error_info(
                title="Not allowed amount",
                content="You can't buy {} stocks".format(num_stock),
            )
        else:
            self._update_trade_state()
            if state == BuyState.BUY_MAXIMUM:
                self.show_warning_info(
                    title="Buy maximum",
                    content="You can only buy {} stocks".format(num_stock),
                )
            else:
                self.show_success_info(
                    title="Buy successfully",
                    content="You have bought {} stocks with {:.2f}".format(
                        num_stock, invested
                    ),
                )
            self.basic_info_component.add_buy_line(self.current_index)

    def on_sell_stock(self):
        self.on_move_next_day()
        num_stock = self.control_pannel.control_command_bar.sell_amount_box.value()
        state, avaliable = self.trade_core.sell(num_stock)
        if state == SellState.SUCCESS:
            self._update_trade_state()
            self.show_success_info(
                title="Sell successfully",
                content="You have sold {} stocks with {:.2f}".format(
                    num_stock, avaliable
                ),
            )
            self.basic_info_component.add_sell_line(self.current_index)
        else:
            self.show_error_info(
                title="Sell failed", content="You don't have enough stocks to sell"
            )

    def on_finish_simulation(self):
        self.control_pannel.control_command_bar.next_day_action.setDisabled(True)
        self.control_pannel.control_command_bar.buy_action.setDisabled(True)
        self.control_pannel.control_command_bar.sell_action.setDisabled(True)
        self.control_pannel.control_command_bar.buy_amount_box.setDisabled(True)
        self.control_pannel.control_command_bar.sell_amount_box.setDisabled(True)
        self.control_pannel.control_command_bar.buy_money_label.setDisabled(True)

    def on_buy_amount_changed(self):
        current_value = self.control_pannel.control_command_bar.buy_amount_box.value()
        if not self.trade_core.is_avaliable_buy_amount(current_value):
            self.show_warning_info(
                title="Unavaliable amount",
                content="You can't buy {} stocks".format(current_value),
            )
        self.control_pannel.control_command_bar.buy_money_label.setText(
            f"≈{self.trade_core.current_price*self.control_pannel.control_command_bar.buy_amount_box.value():.2f}"
        )

    def on_sell_amount_changed(self):
        current_value = self.control_pannel.control_command_bar.sell_amount_box.value()
        if not self.trade_core.is_avaliable_sell_amount(current_value):
            self.show_warning_info(
                title="Unavaliable amount",
                content="You can't sell {} stocks".format(current_value),
            )
