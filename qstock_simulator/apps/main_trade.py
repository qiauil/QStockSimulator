from ..gui.window.trade_window import TradeWindow
from ..components.basic_info import BasicInfoComponent
from ..libs.trade_core import TradeCore, BuyState, SellState
from ..libs.io import save_trade_state
from qstock_plotter.libs.data_handler import DataHandler
from typing import Optional
import os


class MainTrade(TradeWindow):

    def __init__(
        self,
        data_handler: DataHandler,
        start_index: int,
        end_index: int,
        start_trade_index: int,
        trade_core: TradeCore,
        log_file_path: Optional[str] = None,
        show_loading: bool = True,
        parent=None,
    ):  
        super().__init__(show_loading=show_loading,parent=parent)
        # initialze main data
        self.start_index = start_index
        self.end_index = end_index
        self.start_trade_index = start_trade_index

        self.log_file_path=log_file_path
        if self.log_file_path is not None:
            if not os.path.isdir(self.log_file_path):
                raise ValueError("Invalid log file path")
            if not os.path.exists(self.log_file_path):
                os.makedirs(self.log_file_path)
            indicies,avaliable,current,invested,invested_stock,handling_fee_total=self._read_state_log()
            self.setWindowTitle(f"Stock Simulator - {os.path.basename(self.log_file_path)}")
        else:
            indicies = avaliable = current = invested = invested_stock= handling_fee_total = []
            self.setWindowTitle(f"Stock Simulator")
        self.current_index = start_trade_index+len(indicies)

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
                component.initialze(data_handler, start_index, self.current_index)
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
        # trade plot update from log file
        if len(indicies) > 0:
            # update trade core according to log file
            self.trade_core.load_state(
                [state[-1] for state in [avaliable,current,invested,invested_stock,handling_fee_total]]
            )
            # update trade plot according to log file
            self.control_pannel.set_invested_money_plot(indicies,invested)
            self.control_pannel.set_avaliable_money_plot(indicies,avaliable)
            self.control_pannel.set_current_money_plot(indicies,[avaliable[i]+invested[i] for i in range(len(avaliable))])
            self.control_pannel.profit_plot.full_range()
        else:
            # update trade core according to initial setting
            t, initial, close, high, low = self.day_data.prices[self.current_index]
            self.trade_core.current_price = close
            # update trade plot only with the trade core
            self._update_trade_plot()
        # update trade info table according to trade core
        self._update_info_table()
        if self.log_file_path is not None:
            self._read_action_log()
        # other settings
        if self.current_index == self.end_index:
            self.on_finish_simulation()

    @property
    def trade_state_log_path(self):
        if self.log_file_path is None:
            return None
        return os.path.join(self.log_file_path,"state.log")
    
    @property
    def trade_action_log_path(self):
        if self.log_file_path is None:
            return None
        return os.path.join(self.log_file_path,"action.log")

    def _read_state_log(self):
        log_file_path=self.trade_state_log_path
        current=[];invested=[];avaliable=[];invested_stock=[];handling_fee_total=[]
        if not os.path.exists(log_file_path):
            with open(log_file_path,"w") as f:
                f.write("#avaliable_money,current_price,invested_money,invested_stock,handling_fee_total\n")
            return list(range(len(current))),avaliable,current,invested,invested_stock,handling_fee_total
        with open(log_file_path,"r") as f:
            lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and len(line.strip())>0:
                line = line.strip().split(",")
                avaliable.append(float(line[0]))
                current.append(float(line[1]))
                invested.append(float(line[2])) 
                invested_stock.append(float(line[3]))
                handling_fee_total.append(float(line[4]))
        return list(range(len(current))),avaliable,current,invested,invested_stock,handling_fee_total
        
    def _write_state_log(self,
                         log_file_path:str=None):
        log_file_path = log_file_path if log_file_path is not None else self.trade_state_log_path
        if log_file_path is not None:
            try:
                save_trade_state(log_file_path,self.trade_core)
            except Exception as e:
                self.show_error_info(title="Log error",content="Failed to write state log:{}".format(str(e)))

        
    def _read_action_log(self,log_file_path:str=None):
        log_file_path = log_file_path if log_file_path is not None else self.trade_action_log_path
        try:
            if not os.path.exists(log_file_path):
                with open(log_file_path,"w") as f:
                    f.write("#action(buy or sell),day\n")
                return None
            with open(log_file_path,"r") as f:
                lines = f.readlines()
            for line in lines:
                if not line.startswith("#"):
                    line = line.strip().split(",")
                    if line[0] == "b":
                        self.basic_info_component.add_buy_line(int(line[1]))
                    elif line[0] == "s":
                        self.basic_info_component.add_sell_line(int(line[1]))
        except Exception as e:
            self.show_error_info(title="Invalid log file",content="Invalid action log file")

    def _write_action_log(self,action:str,day:int,log_file_path:str=None):
        log_file_path = log_file_path if log_file_path is not None else self.trade_action_log_path
        if log_file_path is not None:
            try:
                if action not in ["b","s"]:
                    self.show_error_info(title="Invalid action",content="Invalid action for log")
                with open(log_file_path,"a") as f:
                    f.write(f"{action},{day}\n")
            except Exception as e:
                self.show_error_info(title="Log error",content="Failed to write action log: {}".format(str(e)))

    def _update_info_table(self):
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
    
    def _update_trade_plot(self):
        self.control_pannel.update_avaliable_money_plot(self.trade_core.avaliable_money)
        self.control_pannel.update_invested_money_plot(self.trade_core.invested_money)
        self.control_pannel.update_current_money_plot(
            self.trade_core.avaliable_money + self.trade_core.invested_money
        )
        self.control_pannel.profit_plot.full_range()

    def _update_trade_state(self):
        self._update_info_table()
        self._update_trade_plot()

    def _move_to_next_day_trade_core(self):
        t, initial, close, high, low = self.day_data.prices[self.current_index]
        self.trade_core.move_to_next_day(close)

    def _move_to_next_day_widget(self):
        self.current_index += 1
        self._update_trade_state()
        self._write_state_log()
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


    def on_move_next_day(self):
        self._move_to_next_day_trade_core()
        self._move_to_next_day_widget()

    def on_buy_stock(self):
        self._move_to_next_day_trade_core()
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
            self._write_action_log("b",self.current_index)
        self._move_to_next_day_widget()

    def on_sell_stock(self):
        self._move_to_next_day_trade_core()
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
            self._write_action_log("s",self.current_index)
        else:
            self.show_error_info(
                title="Sell failed", content="You don't have enough stocks to sell"
            )
        self._move_to_next_day_widget()

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
