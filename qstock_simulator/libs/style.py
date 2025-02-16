import qstock_plotter.libs.style as style
from qstock_plotter.libs.helpers import ConfigurationsHandler
from qstock_plotter.libs.helpers import tuple_to_color,color_to_rbg_tuple
from enum import Enum
from qfluentwidgets import FluentIconBase, getIconColor, Theme
from PyQt6 import QtCore
import os

file_path = os.path.realpath(__file__)
resource_path=os.path.abspath(os.path.join(file_path,os.pardir,os.pardir,"resources"))
QtCore.QDir.addSearchPath('icons', os.path.join(resource_path,"icon")+os.sep)
print(os.path.join(resource_path,"icon"))

def default_style_configs() -> ConfigurationsHandler:
    handler=style.default_style_configs()
    handler.add_config_item("current_money_color",
                            default_value=(23, 195, 178),
                            value_type=tuple,
                            in_func=lambda x,other_config:tuple_to_color(x),out_func=lambda x,other_config:color_to_rbg_tuple(x),
                            description="color of the negative bars")
    handler.add_config_item("invested_money_color",
                            default_value=(195, 23, 178),
                            value_type=tuple,
                            in_func=lambda x,other_config:tuple_to_color(x),out_func=lambda x,other_config:color_to_rbg_tuple(x),
                            description="color of the negative bars")
    handler.add_config_item("avaliable_money_color",
                            default_value=(178, 195, 23),
                            value_type=tuple,
                            in_func=lambda x,other_config:tuple_to_color(x),out_func=lambda x,other_config:color_to_rbg_tuple(x),
                            description="color of the negative bars")
    handler.add_config_item("buy_line_color",
                            default_value=(23, 195, 178),
                            value_type=tuple,
                            in_func=lambda x,other_config:tuple_to_color(x),out_func=lambda x,other_config:color_to_rbg_tuple(x),
                            description="color of the negative bars")
    handler.add_config_item("sell_line_color",
                            default_value=(195, 23, 178),
                            value_type=tuple,
                            in_func=lambda x,other_config:tuple_to_color(x),out_func=lambda x,other_config:color_to_rbg_tuple(x),
                            description="color of the negative bars")
    handler.add_config_item("buy_sell_line_width",
                            default_value=4,
                            value_type=int,
                            description="width of the buy line")
    return handler

def make_style(style_yaml_file="",**kwargs):
    configs_handler=default_style_configs()
    if style_yaml_file != "":
            configs_handler.set_config_items_from_yaml(style_yaml_file)
    configs_handler.set_config_items(**kwargs)
    return configs_handler.configs()

class Icon(FluentIconBase, Enum):

    OPEN = "open"
    NEWPROJECT = "new_project"
    DATA= "data"
    NUMBER="number"
    SELECTED="selected"
    RULER="ruler"
    CODE="Code"
    MONEY="money"

    def path(self, theme=Theme.AUTO):
        return f"icons:{self.value}_{getIconColor(theme)}.svg"
