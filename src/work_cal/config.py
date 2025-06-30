from __future__ import annotations

import re
import tomllib

from pydantic import BaseModel, Field

from work_cal.base import (
    CONFIG_PATH,
    DEFAULT_SHIFT_DURATION,
    DEFAULT_SHIFT_END_HOUR,
    DEFAULT_SHIT_START_HOUR,
    DEFAULT_WORKER_NAME,
)


class HourMinute:
    regex = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

    def __init__(self, value: str) -> None:
        match = self.regex.match(value)
        if not match:
            msg = f"Invalid hour (24h) format: {value}"
            raise ValueError(msg)
        self.value = value
        self.hour = int(match.group(1))
        self.minute = int(match.group(2))

    @classmethod
    def validate(cls, value) -> HourMinute:  # noqa: ANN001
        if isinstance(value, cls):
            return value
        return cls(str(value))


class ShiftType(BaseModel):
    name: str = "Shift"  # should be unique
    end_hour: HourMinute | None = None
    start_hour: HourMinute | None = None
    default_duration_hours: int | None = None
    allowed_week_days: list[int] | None = None


def _default_shit_types_factory() -> list[ShiftType]:
    return [ShiftType()]


class WorkCalConfig(BaseModel):
    worker_name: str = DEFAULT_WORKER_NAME
    default_start_hour: HourMinute = DEFAULT_SHIT_START_HOUR
    default_end_hour: HourMinute = DEFAULT_SHIFT_END_HOUR
    default_duration_hours: int = DEFAULT_SHIFT_DURATION

    shift_types: list[ShiftType] = Field(default_factory=_default_shit_types_factory)


def load_config() -> WorkCalConfig:
    toml_data = tomllib.loads(CONFIG_PATH.read_text("utf-8")) if CONFIG_PATH.exists() else {}

    return WorkCalConfig(**toml_data)
