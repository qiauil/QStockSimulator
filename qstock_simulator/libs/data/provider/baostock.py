from ..handler import DataHandler, BaoStockDataHandler
from ._basis import DataProvider, DataProviderGUISetup
from .._bs_utils import bs_check_error
from ....gui.widget.data_provider_init import BaoStockProviderInitGUI
import baostock as bs
from baostock.data.resultset import ResultData
import datetime
from typing import Optional
import pandas as pd

class BaoStockDataProvider(DataProvider):

    def __init__(self, 
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 ):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        if datetime.datetime.now().date() <= datetime.datetime.strptime(end_date, "%Y-%m-%d").date():
            self.end_date = datetime.datetime.now().date()-datetime.timedelta(days=1)
            self.end_date = self.end_date.strftime("%Y-%m-%d")
        self.latest_trade_date = None

    def on_exit(self):
        pass
        
    def _collect_all(self, result: ResultData) -> list:
        data_list = []
        while (result.error_code == "0") & result.next():
            data_list.append(result.get_row_data())
        return data_list

    def _get_latest_trade_date(self,
                               require_logout=True) -> str:
        logged_in = False
        if self.latest_trade_date is not None:
            return self.latest_trade_date,logged_in
        current_date = datetime.datetime.now().date() if self.end_date is None else self.end_date
        current_date = pd.to_datetime(current_date)
        start_date = current_date - datetime.timedelta(days=30)
        bs_check_error(bs.login())
        logged_in = True
        trade_date = bs_check_error(
            bs.query_trade_dates(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=current_date.strftime("%Y-%m-%d"),
            )
        )
        if require_logout and logged_in:
            bs_check_error(bs.logout())
        for date in reversed(self._collect_all(trade_date)):
            if date[1] == "1":
                self.latest_trade_date = date[0]
                return date[0],logged_in
        raise RuntimeError("No trade date found")

    def get_stock_list(self):
        latest_day, logged_in=self._get_latest_trade_date(require_logout=False)
        if not logged_in:
            bs_check_error(bs.login())
        stock_list = bs_check_error(
            bs.query_all_stock(day=latest_day)
        )
        res = []
        while (stock_list.error_code == "0") & stock_list.next():
            res.append(stock_list.get_row_data()[0])
        bs_check_error(bs.logout())
        return res
    
    def get_data_handler(self, stock_code: str) -> DataHandler:
        return BaoStockDataHandler(stock_code, 
                                   self.start_date,
                                   self.latest_trade_date,
                                   logged_in=False)
    
class BaoStockDataProviderGUISetup(DataProviderGUISetup):

    def __init__(self):
        super().__init__("BaoStock")
        self._gui=None

    def _init_widget(self, parent):
        self._gui = BaoStockProviderInitGUI(parent=parent)
        return self._gui
    
    def get_data_provider(self):
        if self._gui is None:
            raise RuntimeError("GUI not initialized")
        return BaoStockDataProvider(
            self._gui.get_start_date(),
            self._gui.get_end_date(),
        )