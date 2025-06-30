import calendar
from datetime import datetime

import click


@click.command()
@click.argument("month", type=click.IntRange(1, 12))
def main(month: int) -> None:

    year = 2025
    days = [
        f"{year}-{day:02d}-{month:02d}"
        for day in range(1, calendar.monthrange(year, month)[1] + 1)
    ]

    for d in days:
        print(d)


if __name__ == "__main__":
    main()
