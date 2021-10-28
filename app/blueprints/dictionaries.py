import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

dictionaries_bp = Blueprint('dictionaries', __name__)


@dictionaries_bp.route('/dictionary/currency', methods=['GET'])
def get_currencies_list():
    currencies = sqlalchemy_session.query(Currency).all()
    currencies_dict = {currency.id: currency.name for currency in currencies}
    return currencies_dict, 200


@dictionaries_bp.route('/dictionary/countries', methods=['GET'])
def get_countries_list():
    countries = sqlalchemy_session.query(Country).all()
    countries_dict = {country.id: country.name for country in countries}
    return countries_dict, 200


@dictionaries_bp.route('/dictionary/users', methods=['GET'])
def get_users_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(User).all()
        users_dict = {user.id: str(user) for user in users}
        return users_dict, 200
    users = sqlalchemy_session.query(User).where(
        User.first_name.like(f'%{name_fragment}%') | User.last_name.like(f'%{name_fragment}%'))
    users_dict = {user.id: str(user) for user in users}
    return users_dict, 200


@dictionaries_bp.route('/dictionary/managers', methods=['GET'])
def get_managers_dict():
    name_fragment = request.args.get('search', False)
    if not name_fragment:
        users = sqlalchemy_session.query(User).all()
        users_dict = {user.id: str(user) for user in users}
        return users_dict, 200
    users = sqlalchemy_session.query(User).where(User.role != 'user').filter(
        User.first_name.like(f'%{name_fragment}%') | User.last_name.like(f'%{name_fragment}%'))
    users_dict = {user.id: str(user) for user in users}
    return users_dict, 200

