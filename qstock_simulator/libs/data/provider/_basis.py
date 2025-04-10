from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject

class DataProvider(QObject):

    def get_stock_list(self) -> list:
        raise NotImplementedError

    def get_data_handler(self,stock_code:str,**kwargs) -> list:
        raise NotImplementedError

    def on_exit(self):
        pass

class DataProviderGUISetup(QObject):
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