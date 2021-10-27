from flask import Blueprint, request
from app.database.tables_declaration import *
from shortuuid import uuid
from sqlalchemy.exc import IntegrityError, InvalidRequestError

login = Blueprint('login', __name__)


@login.route('/')
def welcome():
    return str(User.get_by_id(1)), 200


@login.route('/register', methods=['POST'])
def register_new_user():
    user_credentials = request.get_json()
    if user_credentials['password'] != user_credentials['retype_password']:
        return {'response': 'Passwords do not match.'}, 401
    user_credentials.update({'role': Role.user, 'is_active': True, 'token': uuid()})
    del user_credentials['retype_password']
    try:
        user = User(**user_credentials)
        sqlalchemy_session.add(user)
        sqlalchemy_session.commit()
        return 'Success.', 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'User with provided email already registered.'}, 409


@login.route('/login', methods=['POST'])
def login_users():
    user_credentials = request.get_json()
    if 'email' in user_credentials.keys():
        try:
            user = User.get_by_email(user_credentials['email'])
        except TypeError or KeyError:
            return {'response': 'Bad request.'}, 400
        if user is None:
            return {'response': 'Cannot find user with provided email.'}
        if user_credentials['password'] != user.password:
            return {'response': 'Bad password.'}
        return {'token': user.token}, 200
    else:
        return {'response': "Wrong input, need 'email' key."}, 400


@login.route('/user', methods=['GET'])
@User.is_logged_in
def get_user_details():
    user = User.get_by_token(request.headers.get('token'))
    return {'response': user.show()}


@login.route('/user', methods=['PUT'])
@User.is_logged_in
def change_user_details():
    user = User.get_by_token(request.headers.get('token'))
    body = request.get_json()
    try:
        user.modify(body)
        return 'Success.', 201
    except InvalidRequestError:
        return 'Fail.', 400

