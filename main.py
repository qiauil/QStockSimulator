from qstock_plotter.libs.data_handler import HDF5Handler, DataHandler
from qstock_simulator.libs.trade_core import TradeCore, ChineseStockMarketTradeCore
import sys
from PyQt6.QtWidgets import QApplication
from qstock_simulator.apps import MainTrade,GUISetup
from qstock_simulator.libs.data import BaoStockDataHandler
from qfluentwidgets import setTheme, Theme

setTheme(Theme.DARK)           

app = QApplication(sys.argv)
data_handler=HDF5Handler("./sample_data/sample_stock_data.h5")

#data_handler = BaoStockDataHandler("sh.600000",start_date="2021-01-01",end_date="2021-12-31")
trade_core = ChineseStockMarketTradeCore(avaliable_money=1000000)
window = MainTrade(
    data_handler=data_handler,
    start_index=5,
    start_trade_index=10,
    end_index=100,
    trade_core=trade_core
)
'''	

#setTheme(Theme.DARK)
window = GUISetup()
'''
window.show()
sys.exit(app.exec())