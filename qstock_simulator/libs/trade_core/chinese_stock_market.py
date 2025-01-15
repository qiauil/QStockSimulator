from ._basis import TradeCore, TradeCoreGUISetup
from ...gui.widget.trade_core_init import ChineseStockMarketTradeCoreInitGUI
from PyQt6.QtWidgets import QWidget
    
class ChineseStockMarketTradeCore(TradeCore):

    def __init__(self,
                avaliable_money:float=0.0,
                 current_price:float=0.0,
                 commission_rate:float=0.0003,
                 min_commission:float=5.0,
                 tax_rate:float=0.001,
                 transfer_fee_rate:float=0.00001,
                 trade_fee_rate:float=0.0000341):
        super().__init__(avaliable_money=avaliable_money,current_price=current_price)
        self.commission_rate = commission_rate
        self.min_commission = min_commission
        self.tax_rate = tax_rate
        self.transfer_fee_rate = transfer_fee_rate
        self.trade_fee_rate = trade_fee_rate

    def handling_fee_buy(self,num_stock:int):
        commission = max(num_stock * self.current_price * self.commission_rate,self.min_commission)
        buy_fee_rate = self.trade_fee_rate + self.transfer_fee_rate
        return commission + buy_fee_rate * num_stock * self.current_price
    
    def handling_fee_sell(self,num_stock:int):
        commission = max(num_stock * self.current_price * self.commission_rate,self.min_commission)
        sell_fee_rate = self.trade_fee_rate + self.transfer_fee_rate + self.tax_rate
        return commission + sell_fee_rate * num_stock * self.current_price
    
    def is_avaliable_buy_amount(self,num_stock:int):
        return super().is_avaliable_buy_amount(num_stock) and num_stock >= 100
    
    def is_avaliable_sell_amount(self,num_stock:int):
        return super().is_avaliable_sell_amount(num_stock) and num_stock >= 100
    
class ChineseStockMarketTradeCoreGUISetup(TradeCoreGUISetup):

    def __init__(self):
        super().__init__("Chinese Stock Market")
        self.widget = None

    def _init_widget(self, parent: QWidget) -> ChineseStockMarketTradeCoreInitGUI:
        self.widget = ChineseStockMarketTradeCoreInitGUI(parent)
        return self.widget
    
    def get_trade_core(self,
                    avaliable_money:float=0.0,
                    current_price:float=0.0)->TradeCore:
        return ChineseStockMarketTradeCore(avaliable_money=avaliable_money,
                                           current_price=current_price,
                                           **self.widget.current_values())