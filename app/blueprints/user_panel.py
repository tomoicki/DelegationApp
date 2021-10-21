import pandas
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from shortuuid import uuid
from app.database.tables_declaration import *


user_panel = Blueprint('user_panel', __name__)


@user_panel.route('/countries', methods=['GET'])
def get_countries_list():
    countries_and_rates = pandas.read_csv('foreign_diet_rate.csv', delimiter=';')
    countries_list = countries_and_rates['Country'].to_list()
    return jsonify(countries_list), 200


@user_panel.route('/delegations', methods=['GET'])
@User.is_logged_in
def user_panel_view():
    user = User.get_by_token(request.headers.get('token'))
    delegations = user.get_user_delegations()
    delegations = [str(delegation) for delegation in delegations]
    return jsonify(delegations), 200


@user_panel.route('/add_delegation', methods=['POST'])
@User.is_logged_in
def add_delegation_request():
    user = User.get_by_token(request.headers.get('token'))
    delegation_details = request.get_json()
    delegation_details['maker_id'] = user.id
    try:
        delegation_to_add = Delegation(**delegation_details)
        sqlalchemy_session.add(delegation_to_add)
        sqlalchemy_session.commit()
        return 'Success.', 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return 'Fail.', 404


@user_panel.route('/modify_delegation', methods=['GET'])
@User.is_logged_in
def show_delegation():
    delegation_to_show = Delegation.get_by_id(request.headers.get('id'))
    if delegation_to_show is None:
        return {'response': "Cannot find delegation with provided ID."}
    return str(delegation_to_show), 200


@user_panel.route('/modify_delegation', methods=['PUT'])
@User.is_logged_in
def modify_delegation():
    body = request.get_json()
    delegation_id = body['id']
    del body['id']
    try:
        Delegation.modify_delegation(delegation_id, body)
        return 'Success.', 201
    except InvalidRequestError:
        return 'Fail.', 404

