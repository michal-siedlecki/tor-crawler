from datetime import datetime


def is_valid_day_month(day: int, month: int) -> bool:
    try:
        datetime(year=2, month=month, day=day)
    except Exception:
        return False
    return True
