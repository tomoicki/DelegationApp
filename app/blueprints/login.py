from flask import Blueprint, request, redirect, url_for
from app.database.create_connection import postgre_session
from app.database.tables_declaration import *

login = Blueprint('login', __name__, template_folder='Templates')


@login.route('/')
def welcome():
    return {'response': 'hiya'}


@login.route('/login', methods=['POST'])
def login_users():
    # user_credentials = request.get_json()
    user_credentials = {'email': 'usr1@itechart.com', 'password': 'right'}
    sqlalchemy_session = postgre_session()
    user = sqlalchemy_session.query(User).filter(User.email == user_credentials['email']).first()
    if user is None:
        return {'response': 'cannot find user with provided email'}
    if user_credentials['password'] != user.password:
        return {'response': 'bad password'}
    return {'token': user.token}


@login.route('/user_panel', methods=['GET', 'POST'])
def user_panel():
    pass
