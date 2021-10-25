import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

lists_bp = Blueprint('lists', __name__)


@lists_bp.route('/countries_dictionary', methods=['GET'])
def get_countries_list():
    countries = sqlalchemy_session.query(Country).all()
    countries_dict = {country.id: country.name for country in countries}
    return countries_dict, 200


@lists_bp.route('/users_dictionary', methods=['GET'])
def get_users_dict():
    users = sqlalchemy_session.query(User).all()
    users_dict = {user.id: str(user) for user in users}
    return users_dict, 200


@lists_bp.route('/managers_dictionary', methods=['GET'])
def get_managers_dict():
    users = sqlalchemy_session.query(User).where(User.role != 'user')
    users_dict = {user.id: str(user) for user in users}
    return users_dict, 200

