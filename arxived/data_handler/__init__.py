from typing import *
from ..helpers import *

class StockValue():
    
    def __init__(self,start,end,lowest,highest) -> None:
        self.start = start
        self.end = end
        self.lowest = lowest
        self.highest = highest
        
class TradingDate():
    
    def __init__(self,year=Optional[int],Month=Optional[int],day=Optional[int],str_date=Optional[str]) -> None:
        if str_date is not None and (year is not None or Month is not None or day is not None):
            raise ValueError("str_date and year,Month,day cannot be set at the same time")
        if str_date is None and (year is None and Month is None and day is None):
            raise ValueError("at least one of str_date and year,Month,day should be set")
        if str_date is not None:
            try:
                self.year,self.Month,self.day = map(int,str_date.split("_"))
            except:
                raise ValueError("str_date should be in the format of 'year_month_day'")
        else:
            self.year = default(year,0)
            self.Month = default(Month,0)
            self.day = default(day,0)

    def __str__(self) -> str:
        return f"{self.year}_{self.Month}_{self.day}"
    
    def str(self):
        return f"{self.year}_{self.Month}_{self.day}"


class StockData():
    
    def __init__(self,stock_name:str,stock_code:str) -> None:
        self.stock_name = stock_name
        self.stock_code = stock_code
    
    def get_day_data(self,date:Optional[TradingDate],index:Optional[int]) -> StockValue:
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_week_data(self,date:Optional[TradingDate],index:Optional[int]) -> StockValue:
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_month_data(self,date:Optional[TradingDate],index:Optional[int]) -> StockValue:
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_year_data(self,date:Optional[TradingDate],index:Optional[int]) -> StockValue:
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_additional_information(self) -> Dict:
        raise NotImplementedError("Subclass must implement abstract method")