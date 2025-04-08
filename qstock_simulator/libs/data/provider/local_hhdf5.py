from ..handler import DataHandler, HDF5Handler
from ._basis import DataProvider, DataProviderGUISetup
from .._bs_utils import bs_check_error
from ....gui.widget.cards import TransparentFolderSelectCard
from PyQt6.QtWidgets import QSizePolicy
import os

class LocalHDF5DataProvider(DataProvider):

    def __init__(self, 
                 local_data_path: str,
                 black_list=["stock_list.h5"],
                 ):
        super().__init__()
        self.dirs=[]
        self.files=[]
        for root, dirs, files in os.walk(local_data_path):
            for file in files:
                if file.endswith('.h5') and file not in black_list:
                    self.dirs.append(root)
                    self.files.append(file[:-3])

    def on_exit(self):
        pass

    def get_stock_list(self):
        return self.files
    
    def get_data_handler(self, 
                         stock_code: str,
                         logged_out_immediately: bool = True
                         ) -> DataHandler:
        path=self.dirs[self.files.index(stock_code)]
        return HDF5Handler(os.path.join(path,stock_code+".h5"))
    
class LocalHDF5DataProviderGUISetup(DataProviderGUISetup):

    def __init__(self):
        super().__init__("LocalHDF5")
        self._gui=None

    def _init_widget(self, parent):
        self._gui = TransparentFolderSelectCard(parent=parent)
        return self._gui
    
    def get_data_provider(self):
        if self._gui is None:
            raise RuntimeError("GUI not initialized")
        return LocalHDF5DataProvider(self._gui.current_folder)