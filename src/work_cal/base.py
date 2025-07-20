import pathlib
from zoneinfo import ZoneInfo

DEFAULT_CONFIG_DIR = pathlib.Path.home() / ".config" / "cal_manager"
DEFAULT_CONFIG_FILENAME: str = "config.toml"
DEFAULT_MONTH_DUMP_LOCATION: pathlib.Path = DEFAULT_CONFIG_DIR / "dumps"
DEFAULT_WORKER_NAME: str = "Worker"
DEFAULT_TIME_ZONE: ZoneInfo = ZoneInfo("Europe/Warsaw")
DEFAULT_FZF_OPTS: str = "--height=~40%"
