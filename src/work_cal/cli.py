import calendar
from datetime import date, datetime

import click

from work_cal.tui.shift_planner import ShiftPlannerApp


def get_dates_for_month(year: int, month: int) -> list[date]:
    days_in_month = calendar.monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, days_in_month + 1)]


@click.command()
@click.argument("month", type=click.IntRange(1, 12))
@click.option("--year", "-y", type=int, default=datetime.now().year, help="Year (default: current year)")  # noqa: DTZ005
def main(month: int, year: int) -> None:
    dates = get_dates_for_month(year, month)
    app = ShiftPlannerApp(dates)
    app.title = "Shift Planner"
    app.sub_title = "Shift Planner"
    app.run()
    app.planner_state.dump_shift_state()


if __name__ == "__main__":
    main()
