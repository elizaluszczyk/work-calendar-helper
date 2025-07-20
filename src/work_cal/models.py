from pydantic import BaseModel


class Shift(BaseModel):
    name: str
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    from_template: str | None
