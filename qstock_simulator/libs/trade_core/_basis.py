from enum import Enum
from PyQt6.QtWidgets import QWidget

class BuyState(Enum):
    SUCCESS = 1
    NOT_ALLOWED_AMOUNT = 2
    BUY_MAXIMUM = 3
    NOT_ENOUGH_MONEY = 4

class SellState(Enum):
    SUCCESS = 1
    NOT_ALLOWED_AMOUNT = 2

class TradeCore():

    def __init__(self,
                 avaliable_money:float=0.0,
                 current_price:float=0.0):
        self.initialize(avaliable_money,current_price)

    def initialize(self,avaliable_money:float,current_price:float=0.0):
        self.initial_money = avaliable_money
        self.avaliable_money = avaliable_money
        self.current_price = current_price
        self.invested_money = 0.0
        self.invested_stock = 0
        self.handling_fee_total = 0.0

    def move_to_next_day(self,next_day_price:float):
        self.current_price = next_day_price
        self.invested_money = self.invested_stock * self.current_price

    def enough_to_buy(self,num_stock:int):
        return self.avaliable_money >= num_stock * self.current_price + self.handling_fee_buy(num_stock)

    def buy(self,num_stock:int)->bool:
        if self.is_avaliable_buy_amount(num_stock):
            if not self.enough_to_buy(num_stock):
                while True:
                    num_stock -=1
                    if self.enough_to_buy(num_stock) and self.is_avaliable_buy_amount(num_stock):
                        state=BuyState.BUY_MAXIMUM
                        break
                    if num_stock <= 0:
                        return BuyState.NOT_ENOUGH_MONEY,0.0
            else:
                state=BuyState.SUCCESS
            self.invested_stock += num_stock
            handle_fee = self.handling_fee_buy(num_stock)
            self.handling_fee_total += handle_fee
            new_invested=num_stock * self.current_price
            self.avaliable_money -= (new_invested + handle_fee)
            self.invested_money += new_invested
            return state,new_invested
        return BuyState.NOT_ALLOWED_AMOUNT,0.0

    def sell(self,num_stock:int)->bool:
        if self.is_avaliable_sell_amount(num_stock):
            self.invested_stock -= num_stock
            handlin_fee = self.handling_fee_sell(num_stock)
            self.handling_fee_total += handlin_fee
            new_available = num_stock * self.current_price
            self.avaliable_money += (new_available - handlin_fee)
            self.invested_money -= new_available
            return SellState.SUCCESS,new_available
        return SellState.NOT_ALLOWED_AMOUNT,0.0

    def handling_fee_buy(self, num_stock:int):
        return 0.0
    
    def handling_fee_sell(self,num_stock:int):
        return 0.0
    
    def is_avaliable_buy_amount(self,num_stock:int):
        return True
    
    def is_avaliable_sell_amount(self,num_stock:int):
        return self.invested_stock >= num_stock
    
class TradeCoreGUISetup():

    def __init__(
        self,
        name: str,
    ):
        self.name = name

    def _init_widget(self, parent: QWidget) -> QWidget:
        raise NotImplementedError

    def get_trade_core(self,
                 avaliable_money:float=0.0,
                 current_price:float=0.0)->TradeCore:
        raise NotImplementedError