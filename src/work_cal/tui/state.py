from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date

    from work_cal.config import WorkCalConfig, ShiftType
    from work_cal.models import Shift


class DayState:  # noqa: B903
    def __init__(self, selected_template: str | None, shift: Shift | None) -> None:
        self.selected_template: str | None = selected_template
        self.shift: Shift | None = shift


class PlannerState:

    def __init__(self, config: WorkCalConfig, dates: list[date]) -> None:
        self.templates = config.shift_types
        self.dates = dates
        self.date_to_shift: dict[date, DayState] = {dt: DayState(None, None) for dt in self.dates}
        self.current_day = dates[0]

    def get_day_state(self, day: date) -> DayState:
        return self.date_to_shift[day]

    def get_current_day_state(self) -> DayState:
        return self.date_to_shift[self.current_day]

    def get_template_from_name(self, template_name: str) -> ShiftType | None:
        for template in self.templates:
            if template.name == template_name:
                return template

        return None
