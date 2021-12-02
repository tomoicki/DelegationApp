from flask import Blueprint
from app.database.tables_declaration import *
from shortuuid import uuid
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import datetime
from datetime import timedelta

login = Blueprint('login', __name__)


@login.route('/', methods=['GET'])
def welcome():
    return str(Users.get_by_id(1)), 200


@login.route('/register', methods=['POST'])
def register_new_user():
    user_credentials = request.get_json()
    if user_credentials['password'] != user_credentials['retype_password']:
        return {'response': 'Passwords do not match.'}, 401
    user_credentials.update({'role': Role.user, 'is_active': True, 'token': uuid()})
    del user_credentials['retype_password']
    try:
        user = Users(**user_credentials)
        sqlalchemy_session.add(user)
        sqlalchemy_session.commit()
        return {'response': 'Success.'}, 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'User with provided email already registered.'}, 409


@login.route('/login', methods=['POST'])
def login_users():
    user_credentials = request.get_json()
    if 'email' in user_credentials.keys():
        try:
            user = Users.get_by_email(user_credentials['email'])
        except TypeError or KeyError:
            return {'response': 'Bad request.'}, 400
        if user is None:
            return {'response': 'Cannot find user with provided email.'}, 403
        if user_credentials['password'] != user.password:
            return {'response': 'Bad password.'}, 401


        # FIXME:
        # Here we are returning a static token, which is assigned to the user
        # and stored inside a DB. Later it is used to recognize a user.
        # This is an over-complicated ugly reimplementation of well known "basic auth"
        # https://en.wikipedia.org/wiki/Basic_access_authentication
        # The main difference - we use some "random" token instead of `f"{user}:{passwd}"` string.
        #
        # Such method might Ok if you run your site under the HTTPS.
        # S is essential here, otherwise token might be easily stolen by sniffing a network.
        # Which is veery serious security issue.
        # 
        # If that is ok - then basic auth should be used instead of reinventing the wheel.
        # All http clients support it, all http-proxies know what to do with it.
        # Browsers will show a password prompt when HTTP server request this auth type.
        # You can be sure that this header will not be logged on some server/proxy. etc.
        # 
        # If some more sophisticted mechanizm is required - tokens can be used.
        # But they should be generated for a some period of time, stored into the DB.
        # Some additional checks might be added - like check token is used only by a single IP etc.
        # Anyway it is better to use existing solution. And of course you can go inside it
        # and look how it is implemented, learn some patterns etc.
        #
        # https://flask-login.readthedocs.io/en/latest/
        # https://pythonhosted.org/Flask-Security/
        #
        # BTW there is more advanced auth method - https://en.wikipedia.org/wiki/Digest_access_authentication

        return {'token': user.token}, 200
    else:
        return {'response': "Wrong input, need 'email' key."}, 400


@login.route('/user', methods=['GET'])
@Users.is_logged_in
def get_user_details():
    user = Users.get_by_token(request.headers.get('token'))
    return {'response': user.show()}


@login.route('/user', methods=['PUT'])
@Users.is_logged_in
def change_user_details():
    user = Users.get_by_token(request.headers.get('token'))
    body = request.get_json()
    try:
        user.modify(body)
        return {'response': 'Success.'}, 201
    except InvalidRequestError:
        return {'response': 'Fail.'}, 400
