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

    from textual import events

    from work_cal.tui.state import PlannerState


class DayListItem(ListItem):

    def __init__(self, representation: Static, day: date) -> None:
        super().__init__(representation)
        self.day: date = day


class DayList(ListView):
    def __init__(self) -> None:
        super().__init__()
        self._planner_state: PlannerState | None = None
        self.day_selected_for_copying: ListItem | None = None

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

    def on_paste_key_pressed(self) -> None:
        if self.day_selected_for_copying is None:
            return

        current_item = self.highlighted_child

        if current_item is None:
            return

        if self.day_selected_for_copying == current_item:
            return

        if not hasattr(self.day_selected_for_copying, "day") or not hasattr(current_item, "day"):
            return

        selected_for_copy_date = self.day_selected_for_copying.day  # pyrefly: ignore
        selected_for_pasting_into_date = current_item.day  # pyrefly: ignore

        shift = self.planner_state.get_day_state(selected_for_copy_date).shift
        self.planner_state.get_day_state(selected_for_pasting_into_date).shift = shift

        self.refresh_item(selected_for_pasting_into_date)
        self.app.notify("Shift pasted")

    def on_yank_key_pressed(self) -> None:
        current_item = self.highlighted_child
        if current_item is None:
            return

        if current_item.has_class("highlighted"):
            current_item.remove_class("highlighted")
            self.day_selected_for_copying = None
        else:
            if self.day_selected_for_copying and self.day_selected_for_copying != current_item:
                self.day_selected_for_copying.remove_class("highlighted")

            current_item.add_class("highlighted")
            self.day_selected_for_copying = current_item

    def on_deselect_key_pressed(self) -> None:
        if self.day_selected_for_copying is None:
            return
        self.day_selected_for_copying.remove_class("highlighted")
        self.day_selected_for_copying = None

    def on_key(self, event: events.Key) -> None:
        if event.key == "y":
            self.on_yank_key_pressed()
        elif event.key == "p":
            self.on_paste_key_pressed()
        elif event.key == "escape":
            self.on_deselect_key_pressed()
