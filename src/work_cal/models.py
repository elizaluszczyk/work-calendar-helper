from dataclasses import dataclass


@dataclass
class Shift:
    name: str
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    from_template: str | None
