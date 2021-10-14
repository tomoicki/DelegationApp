from flask import Blueprint, request
from functools import wraps
from app.database.create_connection import sqlalchemy_session
from app.database.tables_declaration import *

login = Blueprint('login', __name__, template_folder='Templates')


def is_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if get_user_by_token(request.headers.get('token')) is not None:
            return func(*args, **kwargs)
        return "You are not logged in."
    return wrapper


def get_user_by_token(token: str) -> User:
    return sqlalchemy_session.query(User).filter(User.token == token).first()


@login.route('/')
def welcome() -> str:
    return 'hiya'


@login.route('/login', methods=['POST'])
def login_users() -> dict:
    # user_credentials = request.get_json()
    user_credentials = {'email': 'usr@itechart.com', 'password': 'right'}
    user = sqlalchemy_session.query(User).filter(User.email == user_credentials['email']).first()
    if user is None:
        return {'response': 'cannot find user with provided email'}
    if user_credentials['password'] != user.password:
        return {'response': 'bad password'}
    return {'token': user.token}

