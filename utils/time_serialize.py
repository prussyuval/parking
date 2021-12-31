from datetime import datetime


def datetime_to_str(d: datetime) -> str:
    return d.strftime('%d/%m/%Y %H:%M')


def str_to_datetime(s: str) -> datetime:
    return datetime.strptime(s, '%d/%m/%Y %H:%M')


def time_with_dow_to_str(day: int, hour: int, minute: int) -> str:
    return f"{day} {hour}:{minute}"
