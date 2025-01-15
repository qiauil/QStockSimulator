from PyQt6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout
from PyQt6.QtWidgets import QVBoxLayout,QSizePolicy
from qfluentwidgets import  SimpleCardWidget, qconfig, setTheme, setThemeColor
from qstock_plotter.widgets.navigation_widget import PivotInterface
from qstock_plotter.libs.plot_item import get_plot_item, TradeData, HDF5Handler
from qstock_plotter.libs.style import set_background_with_theme
from qstock_plotter import QStockPlotter
from qstock_plotter.libs.plot_item import CandlestickPricesItem,CandlestickVolumeItem
from qstock_plotter.libs.data_handler import PricesDataFrame, VolumeDataFrame
from .stock_info_bar import StockInfoBar

from typing import Optional

class PriceVolumePlotter(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(8)
        self.setLayout(self.main_layout)

        self.price_card = SimpleCardWidget()
        self.price_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.price_card_layout = QVBoxLayout(self.price_card)
        self.price_plotter = QStockPlotter(show_zoom_bar=True)
        self.price_card_layout.addWidget(self.price_plotter)
        self.price_card.setMinimumHeight(300)

        self.volume_card = SimpleCardWidget()
        self.volume_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.volume_card_layout = QVBoxLayout(self.volume_card)
        self.volume_plotter = QStockPlotter(show_zoom_bar=True)
        self.volume_card_layout.addWidget(self.volume_plotter)
        self.volume_card.setMinimumHeight(250)

        self.main_layout.addWidget(self.price_card,stretch=3)
        self.main_layout.addWidget(self.volume_card,stretch=1)

        self.price_plotter.main_plotter.sigViewChanged.connect(
            lambda: self.__on_view_changed(self.price_plotter.main_plotter)
        )
        self.volume_plotter.main_plotter.sigViewChanged.connect(
            lambda: self.__on_view_changed(self.volume_plotter.main_plotter)
        )

        set_background_with_theme(self)

        qconfig.themeChanged.connect(lambda theme: set_background_with_theme(self, theme))

    def __on_view_changed(self, active_plot_widget):
        if active_plot_widget == self.price_plotter.main_plotter:
            self.volume_plotter.update_plot(
                x_loc=active_plot_widget.viewRect().left(),
                x_range=active_plot_widget.viewRect().width(),
            )
        else:
            self.price_plotter.update_plot(
                x_loc=active_plot_widget.viewRect().left(),
                x_range=active_plot_widget.viewRect().width(),
            )

    def plot_price_volume(
        self, price_data: PricesDataFrame, 
        volume_data: VolumeDataFrame
    ):
        price_item = get_plot_item(price_data)
        self.price_plotter.add_main_item(price_item, x_ticks=price_item.get_x_ticks())
        volume_item=get_plot_item(volume_data)
        self.volume_plotter.add_main_item(volume_item, x_ticks=volume_item.get_x_ticks())

    def plot_trade_data(self, trade_data: TradeData):
        self.plot_price_volume(trade_data.prices, trade_data.volume)

    def update_plot(self, x_loc:Optional[float]=None, x_range:Optional[float]=None):
        self.price_plotter.update_plot(x_loc, x_range)

    def set_x_range(self, x_loc:Optional[float]=None, x_range:Optional[float]=None):
        self.price_plotter.set_x_range(x_loc, x_range)
        self.volume_plotter.set_x_range(x_loc, x_range)

    def move_to_end(self):
        self.price_plotter.move_to_end()
    
    def move_to_start(self):
        self.price_plotter.move_to_start()

class PriceVolumeInfoPlotter(PriceVolumePlotter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_bar = StockInfoBar()
        self.main_layout.addWidget(self.info_bar)

    def show_info(self, data_index:int):
        price_item: CandlestickPricesItem = self.price_plotter.main_item
        volume_item: CandlestickVolumeItem = self.volume_plotter.main_item
        price_data: PricesDataFrame = price_item.data
        volume_data: VolumeDataFrame = volume_item.data
        current_time=self.price_plotter.main_item.get_x_ticks()[data_index]
        _, initial_price, end_price, highest_price, lowest_price = price_data[data_index]
        _, volume = volume_data[data_index]
        self.info_bar.set_stock_info(
            time=current_time,
            initial=initial_price,
            end=end_price,
            highest=highest_price,
            lowest=lowest_price,
            volume=volume,
            positive_color=price_item.style.positive_color,
            negative_color=price_item.style.negative_color,
        )



class DWMPriceVolumePlotter(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.day_plotter: Optional[PriceVolumePlotter] = None
        self.week_plotter: Optional[PriceVolumePlotter] = None
        self.month_plotter: Optional[PriceVolumePlotter] = None
        self.data_navigation_widget = PivotInterface()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.data_navigation_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

    def add_day_data(self, 
                     day_data:TradeData
                     ):
        if self.day_plotter is None:
            self.day_plotter = self._create_plotter(parent=self.data_navigation_widget)
            self.day_plotter.price_plotter.set_full_range_enabled(False)
            self.day_plotter.volume_plotter.set_full_range_enabled(False)
            self.data_navigation_widget.addSubInterface(
                self.day_plotter, "Day_plotter", "Day"
            )
        self.day_plotter.plot_trade_data(day_data)

    def add_week_data(self, 
                      week_data: TradeData,
                      ):
        if self.week_plotter is None:
            self.week_plotter = self._create_plotter(parent=self.data_navigation_widget)
            self.week_plotter.price_plotter.set_full_range_enabled(False)
            self.week_plotter.volume_plotter.set_full_range_enabled(False)
            self.data_navigation_widget.addSubInterface(
                self.week_plotter, "Week_plotter", "Week"
            )
        self.week_plotter.plot_trade_data(week_data)

    def add_month_data(self,
                       month_data: TradeData,
                          ):
        if self.month_plotter is None:
            self.month_plotter = self._create_plotter(parent=self.data_navigation_widget)
            self.month_plotter.price_plotter.set_full_range_enabled(False)
            self.month_plotter.volume_plotter.set_full_range_enabled(False)
            self.data_navigation_widget.addSubInterface(
                self.month_plotter, "Month_plotter", "Month"
            )
        self.month_plotter.plot_trade_data(month_data)

    def add_data_handler(self, data_handler: HDF5Handler):
        self.add_day_data(data_handler.day_data)
        self.add_week_data(data_handler.week_data)
        self.add_month_data(data_handler.month_data)
    
    def _create_plotter(self,*args, **kwargs):
        return PriceVolumePlotter(*args, **kwargs)

class DWMPriceVolumeInfoPlotter(DWMPriceVolumePlotter):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.day_plotter: Optional[PriceVolumeInfoPlotter] = None
        self.week_plotter: Optional[PriceVolumeInfoPlotter] = None
        self.month_plotter: Optional[PriceVolumeInfoPlotter] = None

    def _create_plotter(self,*args, **kwargs):
        return PriceVolumeInfoPlotter(*args, **kwargs)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("QStockPlotter")
    sample_stock_data=HDF5Handler("../../../sample_data/sample_stock_data.h5")
    """
    widget=PriceVolumeInfoPlotter()
    widget.plot_trade_data(sample_stock_data.day_data)
    widget.show_info(0)
    """
    #"""
    widget=DWMPriceVolumeInfoPlotter()
    widget.add_data_handler(sample_stock_data)
    widget.day_plotter.show_info(0)
    widget.week_plotter.show_info(0)
    widget.month_plotter.show_info(0)
    #"""
    widget.show()
    #setTheme(Theme.DARK) #switch to dark theme
    #setThemeColor("#0065d5") #change the theme color
    sys.exit(app.exec())