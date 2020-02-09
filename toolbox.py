import re
from datetime import datetime, timezone, timedelta


def get_rightwards_arrow() -> str:
    """
    https://apps.timwhitlock.info/unicode/inspect/hex/27A1
    """
    return "\U000027A1"


def get_south_east_arrow() -> str:
    """
    https://apps.timwhitlock.info/unicode/inspect/hex/2197
    """
    return "\U00002198"


def get_north_east_arrow() -> str:
    """
    https://apps.timwhitlock.info/unicode/inspect/hex/2198
    """
    return "\U00002197"


def get_yesterday_date() -> str:
    return datetime.strftime(datetime.now(timezone.utc) - timedelta(1), "%Y%m%d")


def get_today_date() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d')


def get_today_datetime() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def clean_price(dirty_price):
    """
    Clean the price to facilitate comparisons.
    I've picked dot as decimal separator (e.g. 42.359€)
    Note every prices are supposed to be in euros, multi currencies is not implemented.
    See clean_price_test module for example cases.
    """
    # Handle Mindfactory case: 1.167,83€ (dot is cosmetic separator, comma is the real separator.)
    if "." in dirty_price and "," in dirty_price:
        dirty_price = dirty_price.replace(".", "")
    dirty_price = dirty_price.replace(' ', '')
    m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
    return '{}.{}'.format(m.group(1), m.group(2))
