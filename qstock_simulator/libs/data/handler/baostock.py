from qstock_plotter.libs.data_handler import (
    PricesDataFrame,
    VolumeDataFrame,
    TradeData,
    DataHandler,
)
import baostock as bs
import pandas as pd
from typing import Optional
from .._bs_utils import bs_check_error

class BaoStockDataHandler(DataHandler):

    def __init__(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        logged_in: bool = False,
        logged_out_immediately: bool = True,
    ):
        super().__init__()
        if not logged_in:
            bs_check_error(bs.login())
        self.day_data = self._collect_data(stock_code, start_date, end_date, "d")
        self.week_data = self._collect_data(stock_code, start_date, end_date, "w")
        self.month_data = self._collect_data(stock_code, start_date, end_date, "m")
        if logged_out_immediately:
            bs_check_error(bs.logout())

    def _collect_data(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        frequency="d",
    ):
        rs = bs.query_history_k_data_plus(
            code,
            "date,open,close,high,low,volume",
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag="3",
        )
        price_list = []
        volume_list = []
        while (rs.error_code == "0") & rs.next():
            data = rs.get_row_data()
            price_list.append([data[0], data[1], data[2], data[3], data[4]])
            volume_list.append([data[0], data[5]])
        return TradeData(
            PricesDataFrame(
                pd.DataFrame(
                    price_list, columns=["date", "open", "close", "high", "low"]
                )
            ),
            VolumeDataFrame(pd.DataFrame(volume_list, columns=["date", "volume"])),
        )