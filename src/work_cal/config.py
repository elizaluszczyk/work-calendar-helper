from __future__ import annotations

import re
import tomllib
from typing import Self
from zoneinfo import ZoneInfo  # noqa: TC003 without this pydantic crashes

from pydantic import BaseModel, Field, field_validator

from work_cal.base import (
    DEFAULT_CONFIG_DIR,
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_TIME_ZONE,
    DEFAULT_WORKER_NAME,
)

HOUR_MINUTE_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


def _validate_hour_minute(v: str) -> str:
    parts = v.split(":")

    if len(parts) != 2:  # noqa: PLR2004
        msg = f"Invalid time format: {v}"
        raise ValueError(msg)

    hour, minute = int(parts[0]), int(parts[1])

    if not (0 <= hour <= 23 and 0 <= minute <= 59):  # noqa: PLR2004
        msg = f"Invalid time: {v}"
        raise ValueError(msg)
    return v


class ShiftType(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    name: str = "Shift"  # should be unique
    end_hour: str | None = None
    start_hour: str | None = None
    default_duration_hours: int | None = None
    allowed_week_days: list[int] | None = None

    @field_validator("start_hour", "end_hour")  # pyrefly: ignore
    @classmethod
    def validate_time(cls, v: str | None) -> str | None:
        if v is None:
            return None

        return _validate_hour_minute(v)

    @property
    def end_hour_minute(self) -> int | None:
        if self.end_hour is None:
            return None
        return int(self.end_hour.split(":")[1])

    @property
    def end_hour_hour(self) -> int | None:
        if self.end_hour is None:
            return None
        return int(self.end_hour.split(":")[0])

    @property
    def start_hour_minute(self) -> int | None:
        if self.start_hour is None:
            return None
        return int(self.start_hour.split(":")[1])

    @property
    def start_hour_hour(self) -> int | None:
        if self.start_hour is None:
            return None
        return int(self.start_hour.split(":")[0])


def _default_shit_types_factory() -> list[ShiftType]:
    return [ShiftType()]


class WorkCalConfig(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    worker_name: str = DEFAULT_WORKER_NAME

    shift_types: list[ShiftType] = Field(default_factory=_default_shit_types_factory)
    timezone: ZoneInfo = Field(default=DEFAULT_TIME_ZONE)


def load_config() -> WorkCalConfig:
    config_path = DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILENAME
    toml_data = tomllib.loads(config_path.read_text("utf-8")) if config_path.exists() else {}

    return WorkCalConfig(**toml_data)


class ConfigSingleton:
    _config: WorkCalConfig | None = None

    def __new__(cls) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_config(self) -> WorkCalConfig:
        if self._config is None:
            self._config = load_config()
        return self._config

    def reload_config(self) -> WorkCalConfig:
        self._config = load_config()
        return self._config

    @classmethod
    def reset(cls) -> None:
        if hasattr(cls, "instance"):
            delattr(cls, "instance")
        cls._config = None


def get_config() -> WorkCalConfig:
    return ConfigSingleton().get_config()
