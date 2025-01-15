from .window_basics import ProgressiveWindow
from ...libs.data import DataProvider,DataProviderGUISetup
from ...libs.trade_core import TradeCoreGUISetup
from qfluentwidgets import (
    TitleLabel,
    PushButton,
    PrimaryPushButton,
    FluentStyleSheet,
    ComboBox,
    RadioButton,
    ListWidget,
    HeaderCardWidget,
    SimpleCardWidget,
    BodyLabel,
    ToolButton,
    FluentIcon,
    Slider,
    SpinBox,
    InfoBar,
    InfoBarPosition,
    ScrollArea
)
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QListWidgetItem,QBoxLayout
from typing import Sequence
import random

class _BasicFrame(QWidget):

    def __init__(
        self,
        title: str,
        parent=None,
        next_button_text: str = "Next",
        back_button_text: str = "Back",
        show_back_button: bool = True,
    ):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.title_label = TitleLabel(title, parent=self)
        self.main_layout.addWidget(self.title_label)
        self._scroller=ScrollArea(parent=parent)
        self._scroller.setStyleSheet("background:transparent;border: none;")
        self._scroller_widget = QWidget(parent=self)
        self.content_layout = QVBoxLayout(self._scroller_widget)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(0,10,10,10)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self._scroller)
        self.control_layout = QHBoxLayout()
        self.back_button = PushButton(back_button_text, parent=self)
        self.back_button.setMaximumWidth(100)
        self.next_button = PrimaryPushButton(next_button_text, parent=self)
        self.next_button.setMaximumWidth(100)
        self.next_button.setFocus()
        self.control_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.control_layout.addSpacing(50)
        self.control_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.control_layout.setContentsMargins(0,0,10,0)
        self.main_layout.addLayout(self.control_layout)
        if not show_back_button:
            self.back_button.hide()
        
        self._init_widget()
        self._enable_scroll()

    def _init_widget(self):
        raise NotImplementedError("This method should be implemented in subclass")

    def _enable_scroll(self):
        "scroll is only avaliable when all the wigets are added"
        self._scroller.setWidget(self._scroller_widget)
        self._scroller.setWidgetResizable(True)


    def add_header_card(self, 
                        title:str,
                        widget:QWidget=None,
                        layout:QBoxLayout=None):
        card = HeaderCardWidget(title=title,parent=self)
        self.content_layout.addWidget(card)
        if widget is not None:
            card.viewLayout.addWidget(widget)
        if layout is not None:
            #layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            card.viewLayout.addLayout(layout)
        return card

    @property
    def next_clicked(self):
        return self.next_button.clicked
    
    @property
    def back_clicked(self):
        return self.back_button.clicked
    
class DataProviderInItFrame(_BasicFrame):

    def __init__(self, data_provider_setups:Sequence[DataProviderGUISetup],parent=None):
        self.data_provider_setups = data_provider_setups
        super().__init__(title="Select Data Provider", parent=parent, show_back_button=False)

    def _init_widget(self):
        self._current_provider=None
        self.provider_selector = ComboBox(parent=self)
        self.add_header_card("Select Data Provider",widget=self.provider_selector)
        self.provider_init_stacker = QStackedWidget(self)
        self.add_header_card("Parameters",widget=self.provider_init_stacker)
        for provider_setup in self.data_provider_setups:
            self.provider_init_stacker.addWidget(provider_setup._init_widget(self))
            self.provider_selector.addItem(provider_setup.name)
            self.provider_selector.currentIndexChanged.connect(
                self.provider_init_stacker.setCurrentIndex
            )

    @property
    def current_provider(self)->DataProvider:
        if self._current_provider is None:
            self._current_provider = self.current_provider_setup.get_data_provider()
        return self._current_provider
         
    @property
    def current_provider_setup(self)->DataProviderGUISetup:
        return self.data_provider_setups[self.provider_selector.currentIndex()]
    
    def reset(self):
        if self._current_provider is not None:
            self._current_provider.on_exit()
            self._current_provider = None

class StockSelectorFrame(_BasicFrame):
    def __init__(self,parent=None):
        super().__init__("Select Stock", parent=parent)   
    
    def _init_widget(self):
        self._stock_list=None
        current_stock_card=SimpleCardWidget(parent=self)
        current_stock_card_layout = QHBoxLayout()
        current_stock_card_layout.setContentsMargins(20,20,20,20)
        current_stock_card.setLayout(current_stock_card_layout)
        current_stock_card_layout.addWidget(BodyLabel("Current Stock:"))
        self.current_stock_label = BodyLabel("None")
        current_stock_card_layout.addWidget(self.current_stock_label)
        self.refresh_button = ToolButton(FluentIcon.SYNC, parent=self)
        self.refresh_button.clicked.connect(lambda: self.current_stock_label.setText(random.choice(self.stock_list)))
        current_stock_card_layout.addWidget(self.refresh_button)
        self.content_layout.addWidget(current_stock_card)
        radio_layout = QHBoxLayout()
        self.randomly_select_radio = RadioButton("Random Selected", parent=self)
        self.randomly_select_radio.setChecked(True)
        self.manually_select_radio = RadioButton("Manually Select", parent=self)
        radio_layout.addWidget(self.randomly_select_radio)
        radio_layout.addWidget(self.manually_select_radio)
        self.add_header_card("Stock Select Mode", layout=radio_layout)
        self.stock_list_widget=ListWidget(parent=self)
        self.stock_list_widget.itemClicked.connect(lambda item: self.current_stock_label.setText(item.text()))
        self.list_card=self.add_header_card("Stock List",widget=self.stock_list_widget)
        self.list_card.setMinimumHeight(400)
        self.list_card.setVisible(False)
        self.randomly_select_radio.toggled.connect(self.to_random_select_model)
        self.manually_select_radio.toggled.connect(self.to_manual_select_model)

    @property
    def stock_list(self):
        if self._stock_list is None:
            raise ValueError("Stock list is not set")
        return self._stock_list
    
    def set_stock_list(self,stock_list):
        if len(stock_list)==0:
            print("No stock data available")
            return False
        self._stock_list=stock_list
        self.stock_list_widget.clear()
        for stock in stock_list:
            item = QListWidgetItem(stock)
            self.stock_list_widget.addItem(item)
        self.current_stock_label.setText(random.choice(stock_list))
        return True

    def to_random_select_model(self):
        self.refresh_button.setEnabled(True)
        self.stock_list_widget.clearSelection()
        self.list_card.setVisible(False)
    
    def to_manual_select_model(self):
        self.refresh_button.setEnabled(False)
        self.stock_list_widget.clearSelection()
        self.list_card.setVisible(True)

    @property
    def current_stock(self):
        return self.current_stock_label.text()

class ConfigTradeFrame(_BasicFrame):
    def __init__(self,
                 trade_cores:Sequence[TradeCoreGUISetup],
                 parent=None):
        self.trade_cores=trade_cores
        super().__init__("Trade Configuration", parent=parent,
                         next_button_text="Start Trade")  

    def _init_widget(self):
        trade_simulation_length_layout = QVBoxLayout()
        simulation_length_label=BodyLabel("Trade Simulation Length: 0")
        trade_simulation_length_layout.addWidget(simulation_length_label)
        self.simulation_length_slider = Slider(Qt.Orientation.Horizontal,parent=self)
        self.simulation_length_slider.setRange(1,100)
        self.simulation_length_slider.valueChanged.connect(lambda value: simulation_length_label.setText(f"Trade Simulation Length: {value}"))
        trade_simulation_length_layout.addWidget(self.simulation_length_slider)
        self.add_header_card("Trade Configuration",layout=trade_simulation_length_layout)

        self.trade_core_selector = ComboBox(parent=self)
        self.add_header_card("Select Trade Rule",widget=self.trade_core_selector)
        trade_core_para_layout = QVBoxLayout()
        trade_core_para_layout.setSpacing(0)
        initial_amount_layout = QHBoxLayout()
        initial_amount_layout.setContentsMargins(10,0,10,0)
        initial_amount_label=BodyLabel("Initial avaliable money:")
        initial_amount_label.setMinimumWidth(100)
        initial_amount_layout.addWidget(initial_amount_label)
        self.initial_amount_input = SpinBox(parent=self)
        self.initial_amount_input.setRange(0,100000000)
        self.initial_amount_input.setValue(1000)
        self.initial_amount_input.setFixedWidth(150)
        initial_amount_layout.addWidget(self.initial_amount_input)
        initial_amount_layout.addWidget(BodyLabel("· intial stock price"))
        trade_core_para_layout.addLayout(initial_amount_layout)
        self.trade_core_para_stacker = QStackedWidget(self)
        trade_core_para_layout.addWidget(self.trade_core_para_stacker)
        self.add_header_card("Trade Rule Parameters",layout=trade_core_para_layout)
        for trade_core in self.trade_cores:
            self.trade_core_para_stacker.addWidget(trade_core._init_widget(self))
            self.trade_core_selector.addItem(trade_core.name)
            self.trade_core_selector.currentIndexChanged.connect(
                self.trade_core_para_stacker.setCurrentIndex
            )

    def set_length(self,length:int):
        self.simulation_length_slider.setRange(1,length)
        self.simulation_length_slider.setValue(int(length*0.2))

    def get_trade_core(self,
                       avaliable_money:float=0.0,
                       current_price:float=0.0
                       ):
        return self.trade_cores[self.trade_core_selector.currentIndex()].get_trade_core(
            avaliable_money=avaliable_money,
            current_price=current_price
        )
    
    @property
    def simulation_length(self)->int:
        return self.simulation_length_slider.value()
    
    @property
    def initial_avaliable_amount(self)->float:
        return self.initial_amount_input.value()
    

class DataSelector(ProgressiveWindow):

    def __init__(self, 
                 data_provider_setups: Sequence[DataProviderGUISetup], 
                 trade_core_setups: Sequence[TradeCoreGUISetup],
                 parent=None):
        super().__init__(parent)

        self.stacked_widget = QStackedWidget(self)
        FluentStyleSheet.FLUENT_WINDOW.apply(self.stacked_widget)
        self.main_layout.addWidget(self.stacked_widget)

        self.provider_init = DataProviderInItFrame(data_provider_setups, parent=self)
        self.stacked_widget.addWidget(self.provider_init)

        self.stock_selector = StockSelectorFrame(parent=self)
        self.stacked_widget.addWidget(self.stock_selector)
        self.stock_selector.setVisible(False)

        self.trade_config = ConfigTradeFrame(trade_core_setups,parent=self)
        self.stacked_widget.addWidget(self.trade_config)
        self.trade_config.setVisible(False)

        self.setFixedSize(600, 600)
        self.setResizeEnabled(False)
        self.title_bar.maxBtn.hide()
        #self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
       

    @property
    def current_provider(self)->DataProvider:
        return self.provider_init.current_provider
    
    def show_error_info(self,
                        title:str,
                        content:str,
                        ):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )