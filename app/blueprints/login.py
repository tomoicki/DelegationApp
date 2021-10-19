from flask import Blueprint, request
from app.database.tables_declaration import *

login = Blueprint('login', __name__)


@login.route('/')
def welcome() -> str:
    return 'hiya'


@login.route('/login', methods=['POST'])
def login_users() -> dict:
    user_credentials = request.get_json()
    # user_credentials = {'email': 'maker@gmail.com', 'password': 'right'}
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

