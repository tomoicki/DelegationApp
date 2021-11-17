from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter
from app.database.tables_declaration import *


def id_from_str_to_int(object_dict: dict):
    """Filters by key that contains '_id' and converts the value to int."""
    return {key: (int(value) if '_id' in key else value) for key, value in object_dict.items()}


def currency_factor(currency_from: str, currency_to: str = 'PLN') -> float:
    """Gets currency to currency rate."""
    try:
        factor = CurrencyRates().get_rate(currency_from, currency_to)
    except RatesNotAvailableError:
        c = CurrencyConverter()
        factor = c.convert(1, currency_from, currency_to)
    return factor


def recalculate_hours(hours: float):
    """Provides rate for remaining hours (Data!H1:I5 in excel)."""
    if hours <= 0:
        hour_rate = 0
    elif hours < 8:
        hour_rate = 1/3
    elif hours <= 12:
        hour_rate = 0.5
    else:
        hour_rate = 1
    return hour_rate

