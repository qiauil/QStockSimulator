from ...libs.data import DataProvider, DataProviderGUISetup
from ...libs.trade_core import TradeCoreGUISetup
from qfluentwidgets import (
    ComboBox,
    ListWidget,
    BodyLabel,
    ToolButton,
    FluentIcon,
    Slider,
    SpinBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QListWidgetItem,
)
from typing import Sequence
import random
from ...libs.style import Icon
from ...gui.widget.cards import (
    FolderSelectCard,
    ExpandWidgetCard,
    TransparentWidgetCard,
    WidgetCard,
    LineEditCard,
)
from ...libs.config import cfg
import random, os, datetime

from ...gui.widget.scroller_settings import ScrollerSettings


class DataProviderInItFrame(ScrollerSettings):

    def __init__(
        self, data_provider_setups: Sequence[DataProviderGUISetup], parent=None
    ):
        self.data_provider_setups = data_provider_setups
        super().__init__(
            self.tr("New Project"),
            show_control=True,
            next_button_text=self.tr("Next"),
            show_back_button=False,
            parent=parent,
        )

    def _init_widget(self):
        project_folder_group = self.add_setting_card_group(self.tr("Project Location"))
        self.project_folder_card = FolderSelectCard(
            parent=project_folder_group,
            empty_folder_content=self.tr(
                "No folder selected, will not save the project"
            ),
        )
        self.project_name_card = LineEditCard(
            icon=Icon.CODE,
            title=self.tr("Project Name"),
            content=self.tr("The name of the project"),
            parent=project_folder_group,
        )
        self.project_name_card.line_edit.setPlaceholderText(self.tr("Project Name"))
        self.project_name_card.line_edit.setClearButtonEnabled(True)
        self.project_name_card.setVisible(False)
        if cfg.previous_project_dir.value is not None:
            self.project_folder_card.set_folder(cfg.get(cfg.previous_project_dir))
            self.project_name_card.setVisible(True)
            self.project_name_card.set_text(
                datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            )

        def on_folder_changed(folder: str):
            cfg.set(cfg.previous_project_dir, folder)
            self.project_name_card.setVisible(True)
            if self.project_name_card.text() == "":
                self.project_name_card.set_text(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                )

        self.project_folder_card.sigFolderChanged.connect(on_folder_changed)
        project_folder_group.addSettingCard(self.project_folder_card)
        project_folder_group.addSettingCard(self.project_name_card)

        provider_group = self.add_setting_card_group(self.tr("Data Provider"))
        combo_box_card = ExpandWidgetCard(
            icon=Icon.DATA,
            title=self.tr("Data Provider"),
            content=self.tr("The source of the stock data"),
            parent=provider_group,
        )
        provider_group.addSettingCard(combo_box_card)
        self.provider_selector = ComboBox(parent=combo_box_card)
        combo_box_card.add_widget(self.provider_selector)
        self._current_provider = None
        self.provider_init_stacker = QStackedWidget(self)

        def on_provider_changed(index: int):
            self.provider_init_stacker.setCurrentIndex(index)
            height = self.provider_init_stacker.widget(index).sizeHint().height()
            self.provider_init_stacker.setFixedHeight(height)
            combo_box_card._adjustViewSize()

        for provider_setup in self.data_provider_setups:
            self.provider_init_stacker.addWidget(
                provider_setup._init_widget(parent=self)
            )
            self.provider_selector.addItem(provider_setup.name)
            self.provider_selector.currentIndexChanged.connect(on_provider_changed)
        combo_box_card.add_content_widget(self.provider_init_stacker)
        combo_box_card.setExpand(True)

    @property
    def current_provider(self) -> DataProvider:
        if self._current_provider is None:
            self._current_provider = self.current_provider_setup.get_data_provider()
        return self._current_provider

    @property
    def current_provider_setup(self) -> DataProviderGUISetup:
        return self.data_provider_setups[self.provider_selector.currentIndex()]

    @property
    def project_folder(self):
        if self.project_folder_card.current_folder is None:
            return None
        else:
            if self.project_name_card.text() != "":
                return os.path.join(
                    self.project_folder_card.current_folder,
                    self.project_name_card.text(),
                )
            else:
                raise ValueError(self.tr("Please set the project name"))

    def reset(self):
        if self._current_provider is not None:
            self._current_provider.on_exit()
            self._current_provider = None


class StockSelectorFrame(ScrollerSettings):

    def __init__(self, parent=None):
        super().__init__(
            title=self.tr("New Project"),
            show_control=True,
            parent=parent,
        )

    def _init_widget(self):
        self._stock_list = None
        stock_select_setting_group = self.add_setting_card_group(
            self.tr("Select Stock")
        )
        self.current_stock_card = ExpandWidgetCard(
            icon=Icon.NUMBER,
            title=self.tr("Current Stock"),
            content=self.tr("The stock that will be used for trade"),
            parent=stock_select_setting_group,
        )
        stock_select_setting_group.addSettingCard(self.current_stock_card)
        self.current_stock_card.setExpand(True)
        self.current_stock_label = BodyLabel(self.tr("None"))
        self.current_stock_card.add_widget(self.current_stock_label)
        select_model_widget = QWidget(parent=self.current_stock_card)
        select_model_layout = QHBoxLayout(select_model_widget)
        select_model_comobox = ComboBox(parent=select_model_widget)
        select_model_comobox.addItem(self.tr("Random Selected"))
        select_model_comobox.addItem(self.tr("Manually Select"))
        select_model_comobox.currentIndexChanged.connect(
            lambda index: (
                self.to_random_select_model()
                if index == 0
                else self.to_manual_select_model()
            )
        )
        select_model_layout.addWidget(select_model_comobox)
        self.refresh_button = ToolButton(FluentIcon.SYNC, parent=self)
        self.refresh_button.clicked.connect(
            lambda: self.current_stock_label.setText(random.choice(self.stock_list))
        )
        select_model_layout.addWidget(self.refresh_button)
        select_model_card = TransparentWidgetCard(
            icon=Icon.SELECTED,
            title=self.tr("Select Model"),
            content=self.tr("Select the model randomly or manually"),
            parent=self.current_stock_card,
        )
        select_model_card.add_widget(select_model_widget)
        self.current_stock_card.add_content_widget(select_model_card)
        self.stock_list_widget = ListWidget(parent=self)
        self.stock_list_widget.itemClicked.connect(
            lambda item: self.current_stock_label.setText(item.text())
        )
        self.stock_list_widget.setMinimumHeight(400)
        self.stock_list_widget.setVisible(False)
        # just to avoid the minor bugs in the width
        stock_list_parent_widget = QWidget(parent=self)
        stock_list_parent_layout = QVBoxLayout(stock_list_parent_widget)
        stock_list_parent_layout.addWidget(self.stock_list_widget)
        stock_list_parent_layout.setContentsMargins(0, 0, 10, 0)
        self.current_stock_card.add_content_widget(stock_list_parent_widget)

    @property
    def stock_list(self):
        if self._stock_list is None:
            raise ValueError(self.tr("Stock list is not set"))
        return self._stock_list

    def set_stock_list(self, stock_list):
        self._stock_list = stock_list
        self.stock_list_widget.clear()
        for stock in stock_list:
            item = QListWidgetItem(stock)
            self.stock_list_widget.addItem(item)
        self.current_stock_label.setText(random.choice(stock_list))

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


class ConfigTradeFrame(ScrollerSettings):
    def __init__(self, trade_cores: Sequence[TradeCoreGUISetup], parent=None):
        self.trade_cores = trade_cores
        super().__init__(
            title=self.tr("New Project"),
            next_button_text=self.tr("Start Trade"),
            parent=parent,
        )

    def _init_widget(self):
        simulation_config_group = self.add_setting_card_group(
            self.tr("Simulation Configuration")
        )
        simulation_length_card = WidgetCard(
            icon=Icon.RULER,
            title=self.tr("Simulation Length"),
            content=self.tr("Unit: day"),
            parent=simulation_config_group,
        )
        simulation_config_group.addSettingCard(simulation_length_card)
        self.simulation_length_slider = Slider(Qt.Orientation.Horizontal, parent=self)
        self.simulation_length_slider.setRange(1, 100)
        self.simulation_length_slider.valueChanged.connect(
            lambda value: simulation_length_card.setTitle(
                self.tr("Simulation Length:") + f" {value}"
            )
        )
        self.simulation_length_slider.setMinimumWidth(200)
        simulation_length_card.add_widget(self.simulation_length_slider)

        trade_rule_card = ExpandWidgetCard(
            icon=Icon.CODE,
            title=self.tr("Trade Rule"),
            content=self.tr("The rule for the trade simulation"),
            parent=simulation_config_group,
        )
        simulation_config_group.addSettingCard(trade_rule_card)
        self.trade_core_selector = ComboBox(parent=self)
        trade_rule_card.add_widget(self.trade_core_selector)
        initial_amount_card = TransparentWidgetCard(
            icon=Icon.MONEY,
            title=self.tr("Initial Amount"),
            content=self.tr("× intial stock price"),
            parent=simulation_config_group,
        )
        trade_rule_card.add_content_widget(initial_amount_card)
        self.initial_amount_input = SpinBox(parent=initial_amount_card)
        self.initial_amount_input.setRange(0, 100000000)
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

    def set_length(self, length: int):
        self.simulation_length_slider.setRange(1, length)
        self.simulation_length_slider.setValue(int(length * 0.2))

    def get_trade_core(self, avaliable_money: float = 0.0, current_price: float = 0.0):
        return self.trade_cores[self.trade_core_selector.currentIndex()].get_trade_core(
            avaliable_money=avaliable_money, current_price=current_price
        )

    @property
    def simulation_length(self) -> int:
        return self.simulation_length_slider.value()

    @property
    def initial_avaliable_amount(self) -> float:
        return self.initial_amount_input.value()
