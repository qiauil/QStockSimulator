from ..handler import DataHandler
from PyQt6.QtWidgets import QWidget

class DataProvider:

    def get_stock_list(self) -> list:
        raise NotImplementedError

    def get_data_handler(self,stock_code:str,**kwargs) -> DataHandler:
        raise NotImplementedError

    def on_exit(self):
        pass

class DataProviderGUISetup:
    #SigStockListReady = pyqtSignal()

    def __init__(
        self,
        name: str,
    ):
        self.name = name

    def _init_widget(self, parent: QWidget) -> QWidget:
        raise NotImplementedError

    def get_data_provider(self)->DataProvider:
        raise NotImplementedError