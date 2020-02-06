import re
from datetime import datetime, timezone, timedelta


def get_yesterday_date() -> str:
    return datetime.strftime(datetime.now(timezone.utc) - timedelta(1), "%Y%m%d")


def get_today_date() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d')


def get_today_datetime() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def clean_price(dirty_price):
    """
    Clean the price to facilitate comparisons
    """
    dirty_price = dirty_price.replace(' ', '')
    m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
    return '{}.{}'.format(m.group(1), m.group(2))
