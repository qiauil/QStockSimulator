import yaml
import os
from .data.handler import DataHandler
from .trade_core import TradeCore
from . import trade_core

def save_trade_state(log_file_path: str, trade_core: TradeCore):

    with open(log_file_path, "a") as f:
        f.write(",".join([str(i) for i in trade_core.state()]) + os.linesep)


def read_latest_trade_state(log_file_path: str):
    with open(log_file_path, "r") as f:
        lines = f.readlines()
        while True:
            if len(lines) == 0:
                return None
            if len(lines[-1].strip().split(",")) == 1:
                lines.pop()
            else:
                datas=lines[-1].strip().split(",")
                return [float(i) for i in datas]

def create_project(
    project_dir: str,
    data_handler: DataHandler,
    trade_core: TradeCore,
    start_index: int,
    end_index: int,
    start_trade_index: int,
):
    os.makedirs(project_dir, exist_ok=True)
    if len(os.listdir(project_dir)) > 0:
        raise Exception(f"Project directory {project_dir} is not empty.")
    data_handler.save(os.path.join(project_dir, "stock.h5"))
    trade_core_name = trade_core.__class__.__name__
    trade_core_params = trade_core.collect_init_paras()["params"]
    with open(os.path.join(project_dir, "config.yaml"), "w") as f:
        config={
                "trade_code": {"target": trade_core_name, "params": trade_core_params},
                "start_index": start_index,
                "end_index": end_index,
                "start_trade_index": start_trade_index,
            }
        yaml.safe_dump(
            config,
            f,
        )

def load_project(project_dir: str):
    try:
        data_handler = DataHandler()
        data_handler.load(os.path.join(project_dir, "stock.h5"))
        with open(os.path.join(project_dir, "config.yaml"), "r") as f:
            config = yaml.safe_load(f)
            trade_core_name = config["trade_code"]["target"]
            trade_core_params = config["trade_code"]["params"]
            currenr_trade_core:TradeCore = getattr(trade_core, trade_core_name)(**trade_core_params)
            state_log_path = os.path.join(project_dir, "state.log")
            if os.path.exists(state_log_path):
                trade_state = read_latest_trade_state(state_log_path)
                if trade_state is not None:
                    currenr_trade_core.load_state(trade_state)
        return data_handler, currenr_trade_core, config["start_index"], config["end_index"], config["start_trade_index"]
    except Exception as e:
        raise Exception(f"Error loading project from {project_dir}: {e}")
