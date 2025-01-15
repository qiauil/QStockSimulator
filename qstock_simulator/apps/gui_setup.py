from ..gui.window.data_selector import DataSelector
from ..libs.data.provider import BaoStockDataProviderGUISetup
from ..libs.trade_core import ChineseStockMarketTradeCoreGUISetup
from .main_trade import MainTrade
from PyQt6.QtCore import pyqtSignal
import random
class GUISetup(DataSelector):

    sigShowError = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__([BaoStockDataProviderGUISetup()],
                         [ChineseStockMarketTradeCoreGUISetup()],
                          parent)
        self.data_handler = None
        self.provider_init.next_clicked.connect(self.next_provider_init)
        self.stock_selector.back_clicked.connect(self.back_stock_selector)
        self.stock_selector.next_clicked.connect(self.next_stock_selector)
        self.trade_config.back_clicked.connect(self.back_trade_config)
        self.trade_config.next_clicked.connect(self.next_trade_config)
        self.sigShowError.connect(self.show_error_info)
        
    def next_provider_init(self):
        self.progressive_run(self._next_provider_init, message="Loading stock list...")
    
    def _next_provider_init(self):
        if self.stock_selector.set_stock_list(self.current_provider.get_stock_list()):
            self.stacked_widget.setCurrentWidget(self.stock_selector)
        else:
            self.provider_init.reset()
            self.sigShowError.emit("Error", "No stock data available")

    def back_stock_selector(self):
        self.provider_init.reset()
        self.stacked_widget.setCurrentWidget(self.provider_init)

    def next_stock_selector(self):
        self.progressive_run(self._next_stock_selector,
                             message="Loading stock data...",
                             )
    
    def _next_stock_selector(self):
        self.data_handler = self.current_provider.get_data_handler(self.stock_selector.current_stock)
        self.trade_config.set_length(len(self.data_handler.day_data.prices))
        self.stacked_widget.setCurrentWidget(self.trade_config)

    def back_trade_config(self):
        self.stacked_widget.setCurrentWidget(self.stock_selector)

    def next_trade_config(self):
        total_length = len(self.data_handler.day_data.prices)
        start_trade_index = random.randint(0, total_length-self.trade_config.simulation_length - 1)
        end_index=start_trade_index+self.trade_config.simulation_length
        current_price = self.data_handler.day_data.prices[start_trade_index][2]
        trade_core = self.trade_config.get_trade_core(
            avaliable_money=self.trade_config.initial_avaliable_amount*current_price,
            current_price= current_price,
        )
        self.hide()
        window = MainTrade(data_handler=self.data_handler,
                           start_index=0,
                           current_index=start_trade_index,
                           end_index=end_index,
                           trade_core=trade_core,
                           start_trade_index=start_trade_index,)
        window.show()


    def closeEvent(self, e):
        self.provider_init.reset()
        e.accept()