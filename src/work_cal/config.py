from __future__ import annotations

import re
import tomllib

from pydantic import BaseModel, Field, field_validator

from work_cal.base import (
    CONFIG_PATH,
    DEFAULT_SHIFT_DURATION,
    DEFAULT_SHIFT_END_HOUR,
    DEFAULT_SHIT_START_HOUR,
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


def _default_shit_types_factory() -> list[ShiftType]:
    return [ShiftType()]


class WorkCalConfig(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    worker_name: str = DEFAULT_WORKER_NAME
    default_start_hour: str = DEFAULT_SHIT_START_HOUR
    default_end_hour: str = DEFAULT_SHIFT_END_HOUR
    default_duration_hours: int = DEFAULT_SHIFT_DURATION

    shift_types: list[ShiftType] = Field(default_factory=_default_shit_types_factory)

    @field_validator("default_start_hour", "default_end_hour")  # pyrefly: ignore
    @classmethod
    def validate_time(cls, v: str) -> str:
        return _validate_hour_minute(v)


def load_config() -> WorkCalConfig:
    toml_data = tomllib.loads(CONFIG_PATH.read_text("utf-8")) if CONFIG_PATH.exists() else {}

    return WorkCalConfig(**toml_data)
