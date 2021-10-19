from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from app.database.tables_declaration import *
from shortuuid import uuid

login = Blueprint('login', __name__)


@login.route('/')
def welcome():
    return 'hiya'


@login.route('/register', methods=['POST'])
def register_new_user():
    user_credentials = request.get_json()
    if user_credentials['password'] != user_credentials['retype_password']:
        return {'response': 'Passwords do not match.'}
    user_credentials.update({'role': Role.user, 'is_active': True, 'token': uuid()})
    del user_credentials['retype_password']
    try:
        user = User(**user_credentials)
        sqlalchemy_session.add(user)
        sqlalchemy_session.commit()
        return 'success'
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'User with provided email already registered.'}


@login.route('/login', methods=['POST'])
def login_users():
    user_credentials = request.get_json()
    if 'email' in user_credentials.keys():
        try:
            user = User.get_user_by_email(user_credentials['email'])
        except TypeError or KeyError:
            return {'response': 'bad request'}
        if user is None:
            return {'response': 'cannot find user with provided email'}
        if user_credentials['password'] != user.password:
            return {'response': 'bad password'}
        return {'token': user.token}
    else:
        return {'response': "wrong input, need 'email' key"}

