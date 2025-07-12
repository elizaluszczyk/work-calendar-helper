import calendar
import zoneinfo
from datetime import datetime

import click
import pyfzf

from work_cal.config import WorkCalConfig, ShiftType, load_config


def _get_allowed_shit_types(config: WorkCalConfig, date: datetime) -> list[ShiftType]:
    allowed_shift_types: list[ShiftType] = []

    for shift_type in config.shift_types:
        if shift_type.allowed_week_days is None:
            allowed_shift_types.append(shift_type)
            continue

        if date.weekday() not in shift_type.allowed_week_days:
            continue

        allowed_shift_types.append(shift_type)

    return allowed_shift_types


@click.command()
@click.argument("month", type=click.IntRange(1, 12))
def main(month: int) -> None:
    config = load_config()

    year = 2025
    days = [
        f"{year}-{month:02d}-{day:02d}"
        for day in range(1, calendar.monthrange(year, month)[1] + 1)
    ]

    selected_days = pyfzf.FzfPrompt().prompt(
        days, fzf_options="--multi --layout=reverse",
    )

    for day in selected_days:
        date = datetime.strptime(day, "%Y-%m-%d")  # noqa: DTZ007
        date = date.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Warsaw"))

        allowed_shift_types = _get_allowed_shit_types(config, date)

        print(allowed_shift_types)


if __name__ == "__main__":
    main()
