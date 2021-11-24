from flask import Blueprint
from app.database.tables_declaration import *

dictionaries_bp = Blueprint('dictionaries', __name__)


@dictionaries_bp.route('/dictionary/transit_types', methods=['GET'])
@Users.is_logged_in
def get_transit_types():
    transits = sqlalchemy_session.query(Transit).all()
    transit_types = [{"id": transit.id,  "type": transit.type} for transit in transits]
    return {'response': transit_types}, 200


@dictionaries_bp.route('/dictionary/expense_types', methods=['GET'])
@Users.is_logged_in
def get_expense_types():
    expense_types = [expense_type.value for expense_type in ExpenseType]
    return {'response': expense_types}, 200


@dictionaries_bp.route('/dictionary/user_roles', methods=['GET'])
@Users.is_logged_in
def get_user_roles():
    user_roles = [user_role.value for user_role in Role]
    return {'response': user_roles}, 200


@dictionaries_bp.route('/dictionary/settlement_status_options', methods=['GET'])
@Users.is_logged_in
def get_settlement_status_options():
    settlement_status_options = [settlement_status_option.value for settlement_status_option in SettlementStatusOptions]
    return {'response': settlement_status_options}, 200


@dictionaries_bp.route('/dictionary/currency', methods=['GET'])
@Users.is_logged_in
def get_currencies_list():
    currencies = sqlalchemy_session.query(Currency).all()
    currencies_list = [{"id": str(currency.id), "currency": currency.name} for currency in currencies]
    return {'response': currencies_list}, 200


@dictionaries_bp.route('/dictionary/countries', methods=['GET'])
@Users.is_logged_in
def get_countries_list():
    countries = sqlalchemy_session.query(Country).all()
    countries_list = [{"id": str(country.id), "country": country.name} for country in countries]
    return {'response': countries_list}, 200


@dictionaries_bp.route('/dictionary/users', methods=['GET'])
@Users.is_logged_in
def get_users_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(Users).all()
        users_list = [user.show_id_names() for user in users]
        return {'response': users_list}, 200
    users = sqlalchemy_session.query(Users).where(
        Users.first_name.like(f'%{name_fragment}%') | Users.last_name.like(f'%{name_fragment}%'))
    users_list = [user.show_id_names() for user in users]
    return {'response': users_list}, 200


@dictionaries_bp.route('/dictionary/managers', methods=['GET'])
@Users.is_logged_in
def get_managers_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(Users).where(Users.role != 'user')
        users_list = [user.show_id_names() for user in users]
        return {'response': users_list}, 200
    users = sqlalchemy_session.query(Users).where(Users.role != 'user').filter(
        Users.first_name.like(f'%{name_fragment}%') | Users.last_name.like(f'%{name_fragment}%'))
    users_list = [user.show_id_names() for user in users]
    return {'response': users_list}, 200

