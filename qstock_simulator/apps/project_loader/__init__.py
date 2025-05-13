from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase
from PyQt6.QtWidgets import QWidget
from typing import Sequence
from ...libs.io import create_project
from ..trade_simulator import TradeSimulatorWindow
from ...gui.widget.cards import FolderSelectCard
import os
from ...libs.io import load_project
from ...gui.widget.scroller_settings import ScrollerSettings
from ...gui.window import DefaultWindow


class ProjectLoader(ScrollerSettings):

    def __init__(self, parent_window: QWidget, parent=None):
        self.parent_window = parent_window
        if parent is None:
            parent = parent_window
        super().__init__(
            self.tr("Load Project"),
            True,
            self.tr("Load"),
            show_back_button=False,
            parent=parent,
        )

    def _init_widget(self):
        card_group = self.add_setting_card_group(self.tr("Load Project"))
        self.folder_select_card = FolderSelectCard(self.tr("Select"), parent=self)
        card_group.addSettingCard(self.folder_select_card)
        self.next_button.setEnabled(False)
        self.folder_select_card.sigFolderChanged.connect(self.on_folder_changed)
        self.next_button.clicked.connect(self.load_project)

    def on_folder_changed(self, folder: str):
        files = ["config.yaml", "stock.h5"]
        if not all([os.path.exists(os.path.join(folder, file)) for file in files]):
            self.show_error_info(
                self.tr("Error"),
                self.tr("The selected folder is not a valid project folder"),
            )
            self.folder_select_card.set_folder(None)
        else:
            self.next_button.setEnabled(True)

    def load_project(self):
        data_handler, trade_core, start_index, end_index, start_trade_index = (
            load_project(self.folder_select_card.current_folder)
        )
        from ...gui.window import TitleMenuWindow

        self.parent_window.close()
        main_trade = TradeSimulatorWindow(
            data_handler=data_handler,
            trade_core=trade_core,
            start_index=start_index,
            end_index=end_index,
            start_trade_index=start_trade_index,
            log_file_path=self.folder_select_card.current_folder,
        )
        main_trade.show()
        # self.back_button.setVisible(True)
        # self.back_button.clicked.connect(lambda:main_trade.components[0].widget.day_plotter.move_to_end())
        # self.back_button.clicked.connect(lambda:print(main_trade.components[0].widget.day_plotter.price_plotter.main_plotter.viewRect()))

class ProjectLoaderWindow(DefaultWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().__init__(parent)
        self.setWindowTitle(self.tr("Load Project"))
        self.setMinimumSize(600, 700)
        self.setObjectName("projector_loader_window")
        self.project_loader = ProjectLoader(self, self)
        self.main_layout.addWidget(self.project_loader)
