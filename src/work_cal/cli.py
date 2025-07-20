import calendar
from datetime import date, datetime
from pathlib import Path

import click
from pyfzf.pyfzf import FzfPrompt

from work_cal.base import DEFAULT_FZF_OPTS, DEFAULT_MONTH_DUMP_LOCATION
from work_cal.calendar.shift_parsing import shift_state_dump_to_calendar
from work_cal.models import ShiftStateDump
from work_cal.tui.shift_planner import ShiftPlannerApp


def get_dates_for_month(year: int, month: int) -> list[date]:
    days_in_month = calendar.monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, days_in_month + 1)]


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("month", type=click.IntRange(1, 12))
@click.option("--year", "-y", type=int, default=datetime.now().year, help="Year (default: current year)")  # noqa: DTZ005
def planner(month: int, year: int) -> None:
    dates = get_dates_for_month(year, month)
    app = ShiftPlannerApp(dates)
    app.planner_state.attempt_shift_dump_load()
    app.title = "Shift Planner"
    app.sub_title = "Shift Planner"
    app.run()
    app.planner_state.dump_shift_state()


@main.command()
@click.argument("filename", type=str)
def dump(filename: str) -> None:
    available_dump_files: list[Path] = []
    for path in DEFAULT_MONTH_DUMP_LOCATION.iterdir():
        if not path.is_file():
            continue

        available_dump_files.append(path)

    fzf = FzfPrompt()

    selected_dump_file_list: list[str] = fzf.prompt(available_dump_files, fzf_options=DEFAULT_FZF_OPTS)

    if len(selected_dump_file_list) != 1:
        return

    [selected_dump_file] = selected_dump_file_list

    selected_dump_file = Path(selected_dump_file)

    if selected_dump_file not in available_dump_files:
        msg = "Something went wrong"
        raise RuntimeError(msg)

    json_dump = selected_dump_file.read_text("utf-8")

    shift_state_dump: ShiftStateDump = ShiftStateDump.model_validate_json(json_dump)

    calendar_obj = shift_state_dump_to_calendar(shift_state_dump)

    Path(filename).write_text(calendar_obj.serialize(), encoding="utf-8")


if __name__ == "__main__":
    main()
