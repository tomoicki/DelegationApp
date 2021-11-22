from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter
from app.database.tables_declaration import *


def amount_parser(amount_as_string):
    "xD"
    delimiters = [',', '.']
    if len(amount_as_string) >= 4:
        if amount_as_string[-3] in delimiters:
            listed_amount = amount_as_string.rsplit(amount_as_string[-3], 1)
            centile = listed_amount[1]
            integer = listed_amount[0]
            integer = integer.replace(',', '').replace('.', '')
            amount_as_string = integer + '.' + centile
        else:
            amount_as_string = amount_as_string.replace(',', '').replace('.', '')
    return float(amount_as_string)


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


def recalculate_hours(residue_hours_as_day_fraction: float):
    """Provides rate for remaining hours (Data!H1:I5 in excel)."""
    if residue_hours_as_day_fraction <= 0:
        hour_rate = 0
    elif residue_hours_as_day_fraction <= 1/3:
        hour_rate = 0.5
    else:
        hour_rate = 1
    return hour_rate

