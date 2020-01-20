from datetime import datetime, timezone


def get_today_date() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d')


def get_today_datetime() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
