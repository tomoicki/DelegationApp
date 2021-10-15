from forex_python.converter import CurrencyRates, RatesNotAvailableError
from currency_converter import CurrencyConverter
from app.database.tables_declaration import *


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


foreign_meal_rates = {'breakfast': 0.15, 'lunch': 0.3, 'supper': 0.3}
domestic_meal_rates = {'breakfast': 0.25, 'lunch': 0.5, 'supper': 0.25}


def calculate_diet(number_of_days: int, hours: float, daily_rate: float,
                   meal_list: list[Meal], delegation: Delegation, country: Country) -> float:
    """Calculates diet (D35 in excel) for delegation."""
    if country.name == 'Poland':
        meal_rates = domestic_meal_rates
    else:
        meal_rates = foreign_meal_rates
    meal_cost = [meal_rates[meal_object.type] for meal_object in meal_list]
    delegation.diet = number_of_days * daily_rate + recalculate_hours(hours) * daily_rate - sum(meal_cost)
    return delegation.diet
