from __future__ import annotations

from typing import TYPE_CHECKING

from work_cal.config import get_config
from work_cal.models import ShiftStateDump

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date
    from pathlib import Path

    from work_cal.config import WorkCalConfig, ShiftType
    from work_cal.models import Shift


class DayState:  # noqa: B903
    def __init__(self, selected_template: str | None, shift: Shift | None) -> None:
        self.selected_template: str | None = selected_template
        self.shift: Shift | None = shift


class PlannerState:

    def __init__(self, config: WorkCalConfig, dates: list[date], dump_location: Path | None = None) -> None:

        if dump_location is None:
            dump_location = get_config().month_dump_location
        self.dump_location: Path = dump_location
        self.dump_location.mkdir(exist_ok=True)

        self.templates = config.shift_types
        self.dates = dates
        self.date_to_shift: dict[date, DayState] = {dt: DayState(None, None) for dt in self.dates}
        self.current_day = dates[0]

    def attempt_shift_dump_load(self, filename: str | None = None) -> None:
        if filename is None:
            filename = self._determine_dump_filename(self.date_to_shift)

        dump_path = self.dump_location / filename

        if not dump_path.exists() or not dump_path.is_file():
            return

        json_data = dump_path.read_text(encoding="utf-8")

        dump_data: ShiftStateDump = ShiftStateDump.model_validate_json(json_data)

        for date in dump_data.shift_map:
            if date not in self.date_to_shift:
                return  # if some date from dump is not in date range we skip the whole dump

        for date, shift in dump_data.shift_map.items():
            self.date_to_shift[date].shift = shift
            self.date_to_shift[date].selected_template = shift.from_template

    def get_day_state(self, day: date) -> DayState:
        return self.date_to_shift[day]

    def get_current_day_state(self) -> DayState:
        return self.date_to_shift[self.current_day]

    def get_template_from_name(self, template_name: str) -> ShiftType | None:
        for template in self.templates:
            if template.name == template_name:
                return template

        return None

    @staticmethod
    def _determine_dump_filename(dates: Iterable[date]) -> str:
        year_to_month_map: dict[int, set[int]] = {}
        for date in dates:
            if date.year not in year_to_month_map:
                year_to_month_map[date.year] = set()

            year_to_month_map[date.year].add(date.month)

        filename: str = "shift_dump_"

        for year, months in year_to_month_map.items():
            months_str = "_".join(str(month).rjust(2, "0") for month in sorted(months))
            filename += f"{year}_{months_str}_"

        return filename.strip("_") + ".json"

    def dump_shift_state(self, filename: str | None = None) -> None:
        if filename is None:
            filename = self._determine_dump_filename(self.date_to_shift)

        date_to_shift: dict[date, Shift] = {}
        for day, day_state in self.date_to_shift.items():
            if day_state.shift is None:
                continue

            date_to_shift[day] = day_state.shift

        json_data = ShiftStateDump(shift_map=date_to_shift).model_dump_json()

        (self.dump_location / filename).write_text(json_data, encoding="utf-8")
