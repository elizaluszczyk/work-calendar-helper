import pathlib
from zoneinfo import ZoneInfo

CONFIG_PATH = pathlib.Path.home() / ".config" / "cal_manager" / "config.toml"
DEFAULT_MONTH_DUMP_LOCATION: pathlib.Path = pathlib.Path.home() / ".config" / "cal_manager" / "dumps"
DEFAULT_WORKER_NAME: str = "Worker"
DEFAULT_TIME_ZONE: ZoneInfo = ZoneInfo("Europe/Warsaw")
DEFAULT_FZF_OPTS: str = "--height=~40%"
