from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Footer,
    ListView,
)

from work_cal.config import get_config
from work_cal.tui.day_editor import DayEditor
from work_cal.tui.day_list import DayList, DayListItem
from work_cal.tui.state import PlannerState
from work_cal.tui.themes import themes

if TYPE_CHECKING:
    from datetime import date


class ShiftPlannerApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    .left-panel {
        width: 60%;
        border: solid $primary;
        margin: 1;
    }

    .right-panel {
        width: 40%;
        border: solid $secondary;
        margin: 1;
    }

    Input {
        margin: 0 0 1 0;
    }

    Button {
        margin: 1;
    }

    Select {
        margin: 0 0 1 0;
    }

    .highlighted {
        background: yellow;
    }
    """

    def __init__(self, dates: list[date]) -> None:
        super().__init__()
        self.config = get_config()
        self.planner_state = PlannerState(self.config, dates)

    def compose(self) -> ComposeResult:  # noqa: PLR6301
        with Horizontal():
            with Vertical(classes="left-panel"):
                yield DayEditor()

            with Vertical(classes="right-panel"):
                yield DayList()

        yield Footer()

    def on_mount(self) -> None:
        day_editor = self.query_one(DayEditor)
        day_list = self.query_one(DayList)

        day_editor.set_planner_state(self.planner_state)
        day_list.set_planner_state(self.planner_state)

        for theme in themes:
            self.register_theme(theme)

        self.theme = "ayu_dark"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, DayListItem):
            day_editor = self.query_one(DayEditor)
            self.planner_state.current_day = event.item.day
            day_editor.reload_day()

    def on_day_editor_shift_updated(self, _event: DayEditor.ShiftUpdated) -> None:
        day_list = self.query_one(DayList)
        day_list.refresh_item(self.planner_state.current_day)
