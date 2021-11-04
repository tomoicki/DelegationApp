from flask import Blueprint
from app.database.tables_declaration import *

dictionaries_bp = Blueprint('dictionaries', __name__)


@dictionaries_bp.route('/dictionary/expense_types', methods=['GET'])
def get_expense_types():
    expense_types = [expense_type.value for expense_type in ExpenseType]
    return {'response': expense_types}, 200


@dictionaries_bp.route('/dictionary/user_roles', methods=['GET'])
def get_user_roles():
    user_roles = [user_role.value for user_role in Role]
    return {'response': user_roles}, 200


@dictionaries_bp.route('/dictionary/settlement_status_options', methods=['GET'])
def get_settlement_status_options():
    settlement_status_options = [settlement_status_option.value for settlement_status_option in SettlementStatusOptions]
    return {'response': settlement_status_options}, 200


@dictionaries_bp.route('/dictionary/meal_types', methods=['GET'])
def get_meal_types():
    meal_types = [meal_type.value for meal_type in MealType]
    return {'response': meal_types}, 200


@dictionaries_bp.route('/dictionary/currency', methods=['GET'])
def get_currencies_list():
    currencies = sqlalchemy_session.query(Currency).all()
    currencies_dict = {currency.id: currency.name for currency in currencies}
    return {'response': currencies_dict}, 200


@dictionaries_bp.route('/dictionary/countries', methods=['GET'])
def get_countries_list():
    countries = sqlalchemy_session.query(Country).all()
    countries_dict = {country.id: country.name for country in countries}
    return {'response': countries_dict}, 200


@dictionaries_bp.route('/dictionary/users', methods=['GET'])
def get_users_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(User).all()
        users_dict = {user.id: str(user) for user in users}
        return {'response': users_dict}, 200
    users = sqlalchemy_session.query(User).where(
        User.first_name.like(f'%{name_fragment}%') | User.last_name.like(f'%{name_fragment}%'))
    users_dict = {user.id: str(user) for user in users}
    return {'response': users_dict}, 200


@dictionaries_bp.route('/dictionary/managers', methods=['GET'])
def get_managers_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(User).where(User.role != 'user')
        users_dict = {user.id: str(user) for user in users}
        return {'response': users_dict}, 200
    users = sqlalchemy_session.query(User).where(User.role != 'user').filter(
        User.first_name.like(f'%{name_fragment}%') | User.last_name.like(f'%{name_fragment}%'))
    users_dict = {user.id: str(user) for user in users}
    return {'response': users_dict}, 200

