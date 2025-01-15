from pandas import DataFrame
from .essential_data import HDF5DataFrameHandler

class StockInformation(HDF5DataFrameHandler):
    
    def __init__(self, path_hdf5file: str | None = None, data_frame: DataFrame | None = None) -> None:
        super().__init__(path_hdf5file, "/stock_basic", data_frame)
        self.code=self.data_frame['code'][0]
        self.code_name=self.data_frame['code_name'][0]
        self.ipoDate=self.data_frame['ipoDate'][0]
        self.outDate=self.data_frame['outDate'][0]
        self.type=self.data_frame['type'][0]
        self.status=self.data_frame['status'][0]
        
        
        code	code_name	ipoDate	outDate	type	status
        
        

返回数据说明
参数名称	参数描述
code	证券代码
code_name	证券名称
ipoDate	上市日期
outDate	退市日期
type	证券类型，其中1：股票，2：指数，3：其它，4：可转债，5：ETF
status	上市状态，其中1：上市，0：退市