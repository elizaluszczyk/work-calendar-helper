from __future__ import annotations

import typing
from dataclasses import dataclass
from typing import TYPE_CHECKING

from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import (
    Button,
    Input,
    Select,
    Static,
)

from work_cal.tui.errors import PlannerStateNotSetError
from work_cal.tui.state import PlannerState, Shift

if TYPE_CHECKING:
    from textual.app import ComposeResult


class ShiftParameterError(ValueError):
    def __init__(self, msg: str) -> None:
        self.cause_msg = msg
        super().__init__(msg)


@dataclass
class ShiftBuilder:

    """Validate Shift Data before building.

    After each setter call the relevant internal data is validated. After an error is
    thrown the whole objcet is no longer valid and therefore cannot be used
    """

    name: str | None = None
    start_hour: int | None = None
    start_minute: int | None = None
    end_hour: int | None = None
    end_minute: int | None = None
    from_template: str | None = None

    @staticmethod
    def _validate_hour(hour: int) -> None:
        if hour < 0 or hour > 23:  # noqa: PLR2004
            msg = "Hours must be between 0 and 23"
            raise ShiftParameterError(msg)

    @staticmethod
    def _validate_minute(minute: int) -> None:
        if minute < 0 or minute > 59:  # noqa: PLR2004
            msg = "Minutes must be between 0 and 23"
            raise ShiftParameterError(msg)

    def _validate_timeline(self) -> None:
        if self.end_hour is None or self.start_hour is None:
            return

        msg = "End hour must come after start hour"

        if self.end_hour < self.start_hour:
            raise ShiftParameterError(msg)

        if self.end_hour > self.start_hour:
            return

        # hours are equal

        if self.end_minute is None or self.start_minute is None:
            return

        if self.end_minute < self.start_minute:
            raise ShiftParameterError(msg)

    def set_name(self, name: str) -> ShiftBuilder:
        if len(name) == 0:
            msg = "Name is required"
            raise ShiftParameterError(msg)

        self.name = name
        return self

    def set_start_hour(self, hour: int) -> ShiftBuilder:
        self._validate_hour(hour)
        self.start_hour = hour
        self._validate_timeline()
        return self

    def set_end_hour(self, hour: int) -> ShiftBuilder:
        self._validate_hour(hour)
        self.end_hour = hour
        self._validate_timeline()
        return self

    def set_start_minute(self, minute: int) -> ShiftBuilder:
        self._validate_minute(minute)
        self.start_minute = minute
        self._validate_timeline()
        return self

    def set_end_minute(self, minute: int) -> ShiftBuilder:
        self._validate_minute(minute)
        self.end_minute = minute
        self._validate_timeline()
        return self

    def set_from_template(self, from_template: str) -> ShiftBuilder:
        self.from_template = from_template
        return self

    def build(self) -> Shift:
        for field in (self.name, self.start_hour, self.start_minute, self.end_hour, self.end_minute):
            if field is not None:
                continue

            raise ValueError

        return Shift(
            name=self.name, start_hour=self.start_hour, start_minute=self.start_minute,  # pyrefly: ignore
            end_hour=self.end_hour, end_minute=self.end_minute,  # pyrefly: ignore
            from_template=self.from_template,
        )


class DayEditor(Static):
    def __init__(self) -> None:
        super().__init__()
        self._planner_state: PlannerState | None = None

    def set_planner_state(self, state: PlannerState) -> None:
        self._planner_state = state
        self.reload_day()

    @property
    def planner_state(self) -> PlannerState:
        if self._planner_state is None:
            raise PlannerStateNotSetError

        return self._planner_state

    def compose(self) -> ComposeResult:  # noqa: PLR6301
        with Vertical():
            yield Static("Day Editor", classes="editor-title")
            yield Static("No day selected", id="selected-date")

            yield Select(
                options=[("No Template", None)],
                id="template-select",
                allow_blank=False,
            )

            yield Static("Shift Name:")
            yield Input(placeholder="Enter shift name", id="shift-name")

            with Horizontal():
                with Vertical():
                    yield Static("Start Hour:")
                    yield Input(placeholder="HH", id="start-hour", max_length=2)
                with Vertical():
                    yield Static("Start Minute:")
                    yield Input(placeholder="MM", id="start-minute", max_length=2)

            with Horizontal():
                with Vertical():
                    yield Static("End Hour:")
                    yield Input(placeholder="HH", id="end-hour", max_length=2)
                with Vertical():
                    yield Static("End Minute:")
                    yield Input(placeholder="MM", id="end-minute", max_length=2)

            with Horizontal():
                yield Button("Save Shift", id="save-shift", variant="primary")
                yield Button("Clear Shift", id="clear-shift", variant="error")

    def _update_template_select_for_day(self) -> None:
        day = self.planner_state.current_day
        options: list[tuple[str, str | None]] = [("No Template", None)]

        weekday = day.weekday()

        for tmpl in self.planner_state.templates:
            if tmpl.allowed_week_days is not None and weekday not in tmpl.allowed_week_days:
                continue

            options.append((tmpl.name, tmpl.name))

        template_select = self.query_one("#template-select", Select)
        template_select.set_options(options)

    def reload_day(self) -> None:
        date_display = self.query_one("#selected-date", Static)
        date_display.update(f"Editing: {self.planner_state.current_day.strftime('%A, %B %d, %Y')}")

        self._update_template_select_for_day()

        day_state = self.planner_state.get_current_day_state()

        shift = day_state.shift
        if shift is not None:
            self._update_input("#shift-name", str(shift.name))
            self._update_input("#start-hour", str(shift.start_hour))
            self._update_input("#start-minute", str(shift.start_minute))
            self._update_input("#end-hour", str(shift.end_hour))
            self._update_input("#end-minute", str(shift.end_minute))
        else:
            for selector in ("#shift-name", "#start-hour", "#start-minute", "#end-hour", "#end-minute"):
                self._update_input(selector, "")

    def _update_input(self, input_selector: str, value: str) -> None:
        self.query_one(input_selector, Input).value = value

    def _read_input[ParsedType](
        self,
        input_selector: str,
        factory: typing.Callable[[str], ParsedType],
    ) -> ParsedType | None:
        value = self.query_one(input_selector, Input).value
        if value is None:
            return None

        return factory(value)

    def _read_input_with_default[ParsedType](
        self,
        input_selector: str,
        factory: typing.Callable[[str], ParsedType],
        default: ParsedType,
    ) -> ParsedType:
        input_value_res = self._read_input(input_selector, factory)

        if input_value_res is not None:
            return input_value_res

        return default

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.control.id != "template-select":
            return

        if not isinstance(event.value, str):
            return

        template = self.planner_state.get_template_from_name(event.value)

        if template is None:
            raise RuntimeError  # this should not happen

        self.planner_state.get_current_day_state().selected_template = template.name

        self._update_input("#shift-name", template.name)
        if template.start_hour_hour is not None:
            self._update_input("#start-hour", str(template.start_hour_hour))
        if template.start_hour_minute is not None:
            self._update_input("#start-minute", str(template.start_hour_minute))
        if template.end_hour_hour is not None:
            self._update_input("#end-hour", str(template.end_hour_hour))
        if template.end_hour_minute is not None:
            self._update_input("#end-minute", str(template.end_hour_minute))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-shift":
            self._save_shift()
        elif event.button.id == "clear-shift":
            self._clear_shift()

    def _save_shift(self) -> None:
        """Save the current shift data."""
        try:
            name = self.query_one("#shift-name", Input).value.strip()
            start_hour = int(self.query_one("#start-hour", Input).value or "0")
            start_minute = int(self.query_one("#start-minute", Input).value or "0")
            end_hour = int(self.query_one("#end-hour", Input).value or "0")
            end_minute = int(self.query_one("#end-minute", Input).value or "0")

            current_day_state = self.planner_state.get_current_day_state()

            if not name:
                self.notify("Shift name is required", severity="warning")
                return

            if not (0 <= start_hour <= 23 and 0 <= end_hour <= 23):  # noqa: PLR2004
                self.notify("Hours must be between 0 and 23", severity="error")
                return

            if not (0 <= start_minute <= 59 and 0 <= end_minute <= 59):  # noqa: PLR2004
                self.notify("Minutes must be between 0 and 59", severity="error")
                return

            shift = Shift(
                name=name,
                start_hour=start_hour,
                start_minute=start_minute,
                end_hour=end_hour,
                end_minute=end_minute,
                from_template=current_day_state.selected_template,
            )

            current_day_state.shift = shift
            self.notify(f"Shift saved: {shift.name}", severity="information")

            self.post_message(self.ShiftUpdated())

        except ValueError:
            self.notify("Invalid time values entered", severity="error")

    def _clear_shift(self) -> None:
        day_state = self.planner_state.get_current_day_state()

        day_state.shift = None
        day_state.selected_template = None

        self.notify("Shift cleared", severity="information")
        self.post_message(self.ShiftUpdated())

    class ShiftUpdated(Message):  # noqa: D106
        pass
