from datetime import date, datetime, time

from ics import Calendar, Event

from work_cal.base import DEFAULT_TIME_ZONE
from work_cal.calendar.event import create_calendar_event
from work_cal.models import Shift, ShiftStateDump


def _date_to_datetime(day: date, hour: int, minute: int) -> datetime:
    return datetime.combine(day, time(hour, minute, 0, 0, tzinfo=DEFAULT_TIME_ZONE))


def shift_to_event(day: date, shift: Shift) -> Event:
    start_date = _date_to_datetime(day, shift.start_hour, shift.start_minute)
    end_date = _date_to_datetime(day, shift.end_hour, shift.end_minute)

    return create_calendar_event(start_date, end_date, shift.name)


def shift_state_dump_to_calendar(shift_state: ShiftStateDump, calendar: Calendar | None = None) -> Calendar:
    if calendar is None:
        calendar = Calendar()

    for day, shift in shift_state.shift_map.items():
        calendar.events.add(shift_to_event(day, shift))

    return calendar
