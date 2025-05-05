from ...libs.data import DataProvider, DataProviderGUISetup
from ...libs.trade_core import TradeCoreGUISetup
from qfluentwidgets import (
    FluentStyleSheet,
    InfoBar,
    InfoBarPosition,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)
from typing import Sequence
import random
from ...libs.data.provider import (
    BaoStockDataProviderGUISetup,
    LocalHDF5DataProviderGUISetup,
)
from ...libs.trade_core import ChineseStockMarketTradeCoreGUISetup
from ...libs.io import create_project
from ..trade_simulator import TradeSimulator
from PyQt6.QtCore import pyqtSignal
import random, os

from ._view import DataProviderInItFrame,StockSelectorFrame,ConfigTradeFrame

class DataCreator(QWidget):

    sigShowError = pyqtSignal(str, str)

    def __init__(
        self,
        data_provider_setups: Sequence[DataProviderGUISetup] = [
            BaoStockDataProviderGUISetup(),
            LocalHDF5DataProviderGUISetup(),
        ],
        trade_core_setups: Sequence[TradeCoreGUISetup] = [
            ChineseStockMarketTradeCoreGUISetup()
        ],
        parent_window=None,
        parent=None,
    ):
        super().__init__(parent)
        self.parent_window = parent_window
        self.main_layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget(self)
        FluentStyleSheet.FLUENT_WINDOW.apply(self.stacked_widget)
        self.main_layout.addWidget(self.stacked_widget)

        self.provider_init = DataProviderInItFrame(data_provider_setups, parent=self)
        self.stacked_widget.addWidget(self.provider_init)

        self.stock_selector = StockSelectorFrame(parent=self)
        self.stacked_widget.addWidget(self.stock_selector)
        self.stock_selector.setVisible(False)

        self.trade_config = ConfigTradeFrame(trade_core_setups, parent=self)
        self.stacked_widget.addWidget(self.trade_config)
        self.trade_config.setVisible(False)
        self.data_handler = None
        self.provider_init.next_clicked.connect(self.next_provider_init)
        self.stock_selector.back_clicked.connect(self.back_stock_selector)
        self.stock_selector.next_clicked.connect(self.next_stock_selector)
        self.trade_config.back_clicked.connect(self.back_trade_config)
        self.trade_config.next_clicked.connect(self.next_trade_config)
        self.sigShowError.connect(self.show_error_info)

        self.provider_init.project_folder_card.sigFolderChanged.connect(
            self.on_folder_changed
        )

    def on_folder_changed(self, folder: str):
        if len(os.listdir(folder)) != 0:
            self.sigShowError.emit(
                self.tr("Error"), self.tr("The selected project folder is not empty")
            )
            self.provider_init.project_folder_card.set_folder(None)

    @property
    def project_dir(self):
        return self.provider_init.project_folder

    def progressive_run(self, func, message: str = "Loading...", **kwargs):
        if not hasattr(self.parent_window, "progressive_run"):
            func(**kwargs)
        else:
            self.parent_window.progressive_run(func, message=message, **kwargs)

    def next_provider_init(self):
        self.progressive_run(
            self._next_provider_init, message=self.tr("Loading stock list...")
        )

    def _next_provider_init(self):
        try:
            project_folder = (
                self.provider_init.project_folder
            )  # test whether the name is empty
            stock_list = self.current_provider.get_stock_list()
            if len(stock_list) == 0:
                self.provider_init.reset()
                self.sigShowError.emit(
                    self.tr("Error"), self.tr("No stock data available")
                )
            else:
                self.stock_selector.set_stock_list(stock_list)
                self.stacked_widget.setCurrentWidget(self.stock_selector)
        except Exception as e:
            self.sigShowError.emit(self.tr("Error"), str(e))

    def back_stock_selector(self):
        self.provider_init.reset()
        self.stacked_widget.setCurrentWidget(self.provider_init)

    def next_stock_selector(self):
        self.progressive_run(
            self._next_stock_selector,
            message=self.tr("Loading stock data..."),
        )

    def _next_stock_selector(self):
        self.data_handler = self.current_provider.get_data_handler(
            self.stock_selector.current_stock
        )
        self.trade_config.set_length(len(self.data_handler.day_data.prices))
        self.stacked_widget.setCurrentWidget(self.trade_config)

    def back_trade_config(self):
        self.stacked_widget.setCurrentWidget(self.stock_selector)

    def next_trade_config(self):
        total_length = len(self.data_handler.day_data.prices)
        start_trade_index = random.randint(
            0, total_length - self.trade_config.simulation_length - 1
        )
        end_index = start_trade_index + self.trade_config.simulation_length
        current_price = self.data_handler.day_data.prices[start_trade_index][2].item()
        trade_core = self.trade_config.get_trade_core(
            avaliable_money=self.trade_config.initial_avaliable_amount * current_price,
            current_price=current_price,
        )
        if self.project_dir is not None:
            create_project(
                self.project_dir,
                self.data_handler,
                trade_core,
                start_index=0,
                end_index=end_index,
                start_trade_index=start_trade_index,
            )
        if self.parent_window is not None:
            self.parent_window.hide()
        else:
            self.hide()
        window = TradeSimulator(
            data_handler=self.data_handler,
            start_index=0,
            end_index=end_index,
            trade_core=trade_core,
            start_trade_index=start_trade_index,
            log_file_path=self.project_dir,
        )
        window.show()

    def closeEvent(self, e):
        self.provider_init.reset()
        e.accept()

    @property
    def current_provider(self) -> DataProvider:
        return self.provider_init.current_provider

    def show_error_info(
        self,
        title: str,
        content: str,
    ):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self.parent(),
        )
