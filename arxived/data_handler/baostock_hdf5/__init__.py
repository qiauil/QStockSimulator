from .. import StockData
import pandas as pd
from warnings import warn


class LocalHDF5StockData(StockData):
    
    def __init__(self, path_hdf5:str) -> None:
        self.file_path = path_hdf5
        
        super().__init__(stock_name, stock_code)
    
    def evaluate_local_hdf5(self):
        try:
            hdf =pd.HDFStore(self.file_path, mode='r')
        except Exception as e:
            raise Exception("Failed to open file: "+str(e))
        existed_keys=hdf.keys()
        for key in ['/adjust_factor', '/day_data', '/month_data', '/stock_basic', '/week_data']:
            assert key in existed_keys, f"Key {key} not found in file {self.file_path}"
        for key in [ '/balance_data', '/cash_flow_data', '/dividend_data', '/dupont_data', '/forecast_report', '/growth_data', '/operation_data', '/performance_express_report', '/profit_data']:
            if key in existed_keys:
                warn(f"Key {key} found in file {self.file_path}, but not used in this class")
        hdf.select('/stock_basic')        
        hdf.close()
        
        