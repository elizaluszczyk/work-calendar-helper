from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import (
    ListItem,
    ListView,
    Static,
)

from work_cal.tui.errors import PlannerStateNotSetError

if TYPE_CHECKING:
    from datetime import date

    from work_cal.tui.state import PlannerState


class DayListItem(ListItem):

    def __init__(self, representation: Static, day: date) -> None:
        super().__init__(representation)
        self.day: date = day


class DayList(ListView):
    def __init__(self) -> None:
        super().__init__()
        self._planner_state: PlannerState | None = None

    def set_planner_state(self, state: PlannerState) -> None:
        self._planner_state = state
        self._populate_list()

    @property
    def planner_state(self) -> PlannerState:
        if self._planner_state is None:
            raise PlannerStateNotSetError

        return self._planner_state

    def _populate_list(self) -> None:
        self.clear()
        for target_date in self.planner_state.dates:
            day_data = self.planner_state.get_day_state(target_date)
            day_str = target_date.strftime("%a %m/%d")
            shift_info = f" - {day_data.shift.name}" if day_data.shift is not None else ""
            list_item = DayListItem(Static(f"{day_str}{shift_info}"), target_date)

            self.append(list_item)

    def refresh_item(self, day: date) -> None:
        for item in self.children:
            if not hasattr(item, "day"):
                continue

            if item.day != day:  # pyrefly: ignore
                continue

            day_str = day.strftime("%a %m/%d")
            day_data = self.planner_state.get_day_state(day)
            shift_info = f" - {day_data.shift.name}" if day_data.shift else ""
            item.children[0].update(f"{day_str}{shift_info}")  # pyrefly: ignore
            break
