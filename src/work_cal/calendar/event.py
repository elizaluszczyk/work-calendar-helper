from datetime import datetime

from ics import Event


def create_calendar_event(  # noqa: PLR0913, PLR0917
    start: datetime,
    end: datetime,
    title: str = "Event",
    description: str | None = None,
    location: str | None = None,
    url: str | None = None,
    categories: list | None = None,
) -> Event:
    event = Event()
    event.name = title
    event.begin = start
    event.end = end
    if description:
        event.description = description
    if location:
        event.location = location
    if url:
        event.url = url
    if categories:
        event.categories = set(categories)
    return event
