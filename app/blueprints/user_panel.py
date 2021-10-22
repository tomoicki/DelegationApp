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
    delegations = user.delegation_his
    delegations = [delegation.show() for delegation in delegations]
    return jsonify(delegations), 200


@user_panel.route('/delegations', methods=['POST'])
@User.is_logged_in
def add_delegation_request():
    user = User.get_by_token(request.headers.get('token'))
    delegation_details = request.get_json()
    delegation_details['maker_id'] = user.id
    try:
        Delegation.add(delegation_details)
        return 'Success.', 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return 'Fail.', 404


@user_panel.route('/delegations/<delegation_id>', methods=['GET'])
@User.is_logged_in
def show_delegation(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.worker_id or user.role.value in ['manager', 'hr', 'admin']:
        return str(delegation), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@user_panel.route('/delegations/<delegation_id>', methods=['PUT'])
@User.is_logged_in
def modify_delegation(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    body = request.get_json()
    delegation = Delegation.get_by_id(delegation_id)
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.worker_id or user.role.value in ['manager', 'hr', 'admin']:
        delegation_id = body['id']
        del body['id']
        try:
            Delegation.modify(delegation_id, body)
            return 'Success.', 201
        except InvalidRequestError:
            return 'Fail.', 400
    return {'response': 'You dont have the rights to modify this delegation.'}, 403


@user_panel.route('/delegations/<delegation_id>', methods=['DELETE'])
@User.is_logged_in
def delete_delegation(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.worker_id or user.role.value in ['manager', 'hr', 'admin']:
        try:
            delegation.delete()
            return 'Success.', 201
        except IntegrityError as e:
            sqlalchemy_session.rollback()
            return 'Fail.', 400
    return {'response': 'You dont have the rights to delete this delegation.'}, 403
