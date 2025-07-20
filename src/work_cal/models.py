from datetime import date

from pydantic import BaseModel, Field


class Shift(BaseModel):
    name: str
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    from_template: str | None


class ShiftStateDump(BaseModel):
    shift_map: dict[date, Shift] = Field(default_factory=dict)
