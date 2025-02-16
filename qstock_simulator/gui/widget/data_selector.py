from ...libs.data import DataProvider,DataProviderGUISetup
from ...libs.trade_core import TradeCoreGUISetup
from qfluentwidgets import (
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
    ScrollArea,
    TitleLabel,
    SettingCardGroup,
)
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QSizePolicy,QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QListWidgetItem, QBoxLayout
from typing import Sequence
import random
from .progress_message_box import ProgressMessageBox
from ...libs.data.provider import BaoStockDataProviderGUISetup
from ...libs.trade_core import ChineseStockMarketTradeCoreGUISetup
from ...libs.io import create_project
from ...apps.main_trade import MainTrade
from ...libs.style import Icon
from .cards import FolderSelectCard, ExpandWidgetCard, TransparentWidgetCard, WidgetCard
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
import random,os
from typing import Optional

class _BasicFrame(QWidget):

    def __init__(
        self,
        parent=None,
        next_button_text: str = "Next",
        back_button_text: str = "Back",
        show_back_button: bool = True,
    ):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0,0,0,0)

        self._scroller=ScrollArea(parent=parent)
        self._scroller.setStyleSheet("background:transparent;border: none;")
        self._scroller_widget = QWidget(parent=self)
        self.content_layout = QVBoxLayout(self._scroller_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0,0,15,0)
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
        self.control_layout.setContentsMargins(0,0,15,0)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addSpacing(10)
        if not show_back_button:
            self.back_button.hide()

        self.n_title = 0
        
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
        super().__init__(parent=parent, show_back_button=False)

    def _init_widget(self):
        project_folder_group = SettingCardGroup(
            "Project Location",
            parent=self._scroller_widget)
        self.content_layout.addWidget(project_folder_group,alignment=Qt.AlignmentFlag.AlignTop)
        self.project_folder_card = FolderSelectCard(parent=project_folder_group,empty_folder_content="No folder selected, will not save the project")
        project_folder_group.addSettingCard(self.project_folder_card)

        self.content_layout.addSpacing(20)

        provider_group = SettingCardGroup(
            "Data Provider",
            parent=self._scroller_widget)
        self.content_layout.addWidget(provider_group, alignment=Qt.AlignmentFlag.AlignTop)
        combo_box_card = ExpandWidgetCard(
            icon=Icon.DATA,
            title="Data Provider",
            content="The source of the stock data",
            parent=provider_group
        )
        provider_group.addSettingCard(combo_box_card)
        self.provider_selector = ComboBox(parent=combo_box_card)
        combo_box_card.add_widget(self.provider_selector)
        self._current_provider=None
        self.provider_init_stacker = QStackedWidget(self)
        for provider_setup in self.data_provider_setups:
            self.provider_init_stacker.addWidget(provider_setup._init_widget(self))
            self.provider_selector.addItem(provider_setup.name)
            self.provider_selector.currentIndexChanged.connect(
                self.provider_init_stacker.setCurrentIndex
            )
        combo_box_card.add_content_widget(self.provider_init_stacker)
        combo_box_card.setExpand(True)

    @property
    def current_provider(self)->DataProvider:
        if self._current_provider is None:
            self._current_provider = self.current_provider_setup.get_data_provider()
        return self._current_provider
         
    @property
    def current_provider_setup(self)->DataProviderGUISetup:
        return self.data_provider_setups[self.provider_selector.currentIndex()]

    @property
    def project_folder(self):
        return self.project_folder_card.current_folder

    def reset(self):
        if self._current_provider is not None:
            self._current_provider.on_exit()
            self._current_provider = None

class StockSelectorFrame(_BasicFrame):
    def __init__(self,parent=None):
        super().__init__(parent=parent)   
    
    def _init_widget(self):
        self._stock_list=None
        stock_select_setting_groups=SettingCardGroup(
            "Select Stock",
            parent=self._scroller_widget
        )
        self.content_layout.addWidget(stock_select_setting_groups)
        self.current_stock_card=ExpandWidgetCard(
            icon=Icon.NUMBER,
            title="Current Stock",
            content="The stock that will be used for trade",
            parent=stock_select_setting_groups
        )
        stock_select_setting_groups.addSettingCard(self.current_stock_card)
        self.current_stock_card.setExpand(True)
        self.current_stock_label = BodyLabel("None")
        self.current_stock_card.add_widget(self.current_stock_label)
        select_model_widget = QWidget(parent=self.current_stock_card)
        select_model_layout = QHBoxLayout(select_model_widget)
        select_model_comobox = ComboBox(parent=select_model_widget)
        select_model_comobox.addItem("Random Selected")
        select_model_comobox.addItem("Manually Select")
        select_model_comobox.currentIndexChanged.connect(
            lambda index: self.to_random_select_model() if index==0 else self.to_manual_select_model()
        )
        select_model_layout.addWidget(select_model_comobox)
        self.refresh_button = ToolButton(FluentIcon.SYNC, parent=self)
        self.refresh_button.clicked.connect(lambda: self.current_stock_label.setText(random.choice(self.stock_list)))
        select_model_layout.addWidget(self.refresh_button)
        select_model_card=TransparentWidgetCard(icon=Icon.SELECTED,
                                                title="Select Model",
                                                content="Select the model randomly or manually",
                                                parent=self.current_stock_card)
        select_model_card.add_widget(select_model_widget)
        self.current_stock_card.add_content_widget(select_model_card)
        self.stock_list_widget=ListWidget(parent=self)
        self.stock_list_widget.itemClicked.connect(lambda item: self.current_stock_label.setText(item.text()))
        self.stock_list_widget.setMinimumHeight(400)
        self.stock_list_widget.setVisible(False)
        # just to avoid the minor bugs in the width
        stock_list_parent_widget = QWidget(parent=self)
        stock_list_parent_layout = QVBoxLayout(stock_list_parent_widget)
        stock_list_parent_layout.addWidget(self.stock_list_widget)
        stock_list_parent_layout.setContentsMargins(0,0,10,0)
        self.current_stock_card.add_content_widget(stock_list_parent_widget)


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
        self.stock_list_widget.setVisible(False)
        self.current_stock_card._adjustViewSize()
    
    def to_manual_select_model(self):
        self.refresh_button.setEnabled(False)
        self.stock_list_widget.clearSelection()
        self.stock_list_widget.setVisible(True)
        self.current_stock_card._adjustViewSize()
        
    @property
    def current_stock(self):
        return self.current_stock_label.text()

class ConfigTradeFrame(_BasicFrame):
    def __init__(self,
                 trade_cores:Sequence[TradeCoreGUISetup],
                 parent=None):
        self.trade_cores=trade_cores
        super().__init__(parent=parent,
                         next_button_text="Start Trade")  

    def _init_widget(self):
        simulation_config_group = SettingCardGroup(
            "Simulation Configuration",
            parent=self._scroller_widget
        )
        self.content_layout.addWidget(simulation_config_group)
        simulation_length_card = WidgetCard(
            icon=Icon.RULER,
            title="Simulation Length",
            content="Unit: day",
            parent=simulation_config_group
        )
        simulation_config_group.addSettingCard(simulation_length_card)
        self.simulation_length_slider = Slider(Qt.Orientation.Horizontal,parent=self)
        self.simulation_length_slider.setRange(1,100)
        self.simulation_length_slider.valueChanged.connect(lambda value: simulation_length_card.setTitle(f"Simulation Length: {value}"))
        self.simulation_length_slider.setMinimumWidth(200)
        simulation_length_card.add_widget(self.simulation_length_slider)

        trade_rule_card=ExpandWidgetCard(
            icon=Icon.CODE,
            title="Trade Rule",
            content="The rule for the trade simulation",
            parent=simulation_config_group
        )
        simulation_config_group.addSettingCard(trade_rule_card)
        self.trade_core_selector = ComboBox(parent=self)
        trade_rule_card.add_widget(self.trade_core_selector)
        initial_amount_card=TransparentWidgetCard(
            icon=Icon.MONEY,
            title="Initial Amount",
            content="× intial stock price",
            parent=simulation_config_group
        )
        trade_rule_card.add_content_widget(initial_amount_card)
        self.initial_amount_input = SpinBox(parent=initial_amount_card)
        self.initial_amount_input.setRange(0,100000000)
        self.initial_amount_input.setValue(1000)
        initial_amount_card.add_widget(self.initial_amount_input)
        self.trade_core_para_stacker = QStackedWidget(self)
        for trade_core in self.trade_cores:
            self.trade_core_para_stacker.addWidget(trade_core._init_widget(self))
            self.trade_core_selector.addItem(trade_core.name)
            self.trade_core_selector.currentIndexChanged.connect(
                self.trade_core_para_stacker.setCurrentIndex
            )
        trade_rule_card.add_content_widget(self.trade_core_para_stacker)
        trade_rule_card.setExpand(True)
        self.initial_amount_input.setFixedWidth(150)

        #trade_simulation_length_layout = QVBoxLayout()
        #simulation_length_label=BodyLabel("Trade Simulation Length: 0")
        #trade_simulation_length_layout.addWidget(simulation_length_label)
        #self.simulation_length_slider = Slider(Qt.Orientation.Horizontal,parent=self)
        #self.simulation_length_slider.setRange(1,100)
        #self.simulation_length_slider.valueChanged.connect(lambda value: simulation_length_label.setText(f"Trade Simulation Length: {value}"))
        #trade_simulation_length_layout.addWidget(self.simulation_length_slider)
        #self.add_header_card("Trade Configuration",layout=trade_simulation_length_layout)

        #self.trade_core_selector = ComboBox(parent=self)
        #self.add_header_card("Select Trade Rule",widget=self.trade_core_selector)
        #trade_core_para_layout = QVBoxLayout()
        #trade_core_para_layout.setSpacing(0)
        #initial_amount_layout = QHBoxLayout()
        #initial_amount_layout.setContentsMargins(10,0,10,0)
        #initial_amount_label=BodyLabel("Initial avaliable money:")
        #initial_amount_label.setMinimumWidth(100)
        #initial_amount_layout.addWidget(initial_amount_label)
        #self.initial_amount_input = SpinBox(parent=self)
        #self.initial_amount_input.setRange(0,100000000)
        #self.initial_amount_input.setValue(1000)
        #self.initial_amount_input.setFixedWidth(150)
        #initial_amount_layout.addWidget(self.initial_amount_input)
        #initial_amount_layout.addWidget(BodyLabel("· intial stock price"))
        #trade_core_para_layout.addLayout(initial_amount_layout)
        #self.trade_core_para_stacker = QStackedWidget(self)
        #trade_core_para_layout.addWidget(self.trade_core_para_stacker)
        #self.add_header_card("Trade Rule Parameters",layout=trade_core_para_layout)
        #for trade_core in self.trade_cores:
        #    self.trade_core_para_stacker.addWidget(trade_core._init_widget(self))
        #    self.trade_core_selector.addItem(trade_core.name)
        #    self.trade_core_selector.currentIndexChanged.connect(
        #        self.trade_core_para_stacker.setCurrentIndex
        #    )

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
    

class DataSelector(QWidget):

    sigShowError = pyqtSignal(str, str)

    def __init__(self, 
                 project_dir:Optional[str]=None,
                 data_provider_setups: Sequence[DataProviderGUISetup]=[BaoStockDataProviderGUISetup()], 
                 trade_core_setups: Sequence[TradeCoreGUISetup]=[ChineseStockMarketTradeCoreGUISetup()],
                 parent_window=None,
                 parent=None):   
        super().__init__(parent)
        self.parent_window = parent_window
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10,0,0,0)
        self.main_layout.addWidget(TitleLabel("New Project", parent=self))
        self.main_layout.addSpacing(10)
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
        self.data_handler = None
        self.provider_init.next_clicked.connect(self.next_provider_init)
        self.stock_selector.back_clicked.connect(self.back_stock_selector)
        self.stock_selector.next_clicked.connect(self.next_stock_selector)
        self.trade_config.back_clicked.connect(self.back_trade_config)
        self.trade_config.next_clicked.connect(self.next_trade_config)
        self.sigShowError.connect(self.show_error_info)

        self.provider_init.project_folder_card.sigFolderChanged.connect(self.on_folder_changed)

    def on_folder_changed(self,folder:str):
        if len(os.listdir(folder))!=0:
            self.sigShowError.emit("Error", "The selected project folder is not empty")
            self.provider_init.project_folder_card.set_folder(None)

    @property
    def project_dir(self):
        return self.provider_init.project_folder

    def progressive_run(self, func,
                        message: str="Loading...",
                        **kwargs):
        if not hasattr(self.parent_window,"progressive_run"):
            func(**kwargs)
        else:
            self.parent_window.progressive_run(func, message=message, **kwargs)
        
    def next_provider_init(self):
        self.progressive_run(self._next_provider_init, message="Loading stock list...")
    
    def _next_provider_init(self):
        if self.stock_selector.set_stock_list(self.current_provider.get_stock_list()):
            self.stacked_widget.setCurrentWidget(self.stock_selector)
        else:
            self.provider_init.reset()
            self.sigShowError.emit("Error", "No stock data available")

    def back_stock_selector(self):
        self.provider_init.reset()
        self.stacked_widget.setCurrentWidget(self.provider_init)

    def next_stock_selector(self):
        self.progressive_run(self._next_stock_selector,
                             message="Loading stock data...",
                             )
    
    def _next_stock_selector(self):
        self.data_handler = self.current_provider.get_data_handler(self.stock_selector.current_stock)
        self.trade_config.set_length(len(self.data_handler.day_data.prices))
        self.stacked_widget.setCurrentWidget(self.trade_config)

    def back_trade_config(self):
        self.stacked_widget.setCurrentWidget(self.stock_selector)

    def next_trade_config(self):
        total_length = len(self.data_handler.day_data.prices)
        start_trade_index = random.randint(0, total_length-self.trade_config.simulation_length - 1)
        end_index=start_trade_index+self.trade_config.simulation_length
        current_price = self.data_handler.day_data.prices[start_trade_index][2].item()
        trade_core = self.trade_config.get_trade_core(
            avaliable_money=self.trade_config.initial_avaliable_amount*current_price,
            current_price= current_price,
        )
        if self.project_dir is not None:
            create_project(self.project_dir,
                           self.data_handler,
                           trade_core,
                           start_index=0,
                           end_index=end_index,
                           current_index=start_trade_index,
                           start_trade_index=start_trade_index)
        if self.parent_window is not None:
            self.parent_window.hide()
        else:
            self.hide()
        window = MainTrade(data_handler=self.data_handler,
                           start_index=0,
                           current_index=start_trade_index,
                           end_index=end_index,
                           trade_core=trade_core,
                           start_trade_index=start_trade_index,
                           log_file_path=self.project_dir)
        window.show()


    def closeEvent(self, e):
        self.provider_init.reset()
        e.accept()

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
            parent=self.parent()
        )