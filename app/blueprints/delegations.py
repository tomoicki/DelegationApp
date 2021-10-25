import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

delegations_bp = Blueprint('delegations', __name__)


@delegations_bp.route('/delegations', methods=['GET'])
@User.is_logged_in
def user_panel_view():
    user = User.get_by_token(request.headers.get('token'))
    delegations_list = user.delegation_his
    delegations_list = [delegation.show() for delegation in delegations_list]
    return jsonify(delegations_list), 200


@delegations_bp.route('/delegations', methods=['POST'])
@User.is_logged_in
def add_delegation():
    creator = User.get_by_token(request.headers.get('token'))
    delegation_details = request.get_json()
    delegation_details['creator_id'] = creator.id
    delegation_details['submit_date'] = datetime.datetime.now()
    try:
        Delegation.create(delegation_details)
        return 'Success.', 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return 'Fail.', 404


@delegations_bp.route('/delegations/<delegation_id>', methods=['GET'])
@User.is_logged_in
def show_delegation(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        return jsonify(delegation.details()), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@delegations_bp.route('/delegations/<delegation_id>', methods=['PUT'])
@User.is_logged_in
def modify_delegation(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    body = request.get_json()
    delegation = Delegation.get_by_id(delegation_id)
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        try:
            delegation.modify(body)
            return 'Success.', 201
        except InvalidRequestError:
            return 'Fail.', 400
    return {'response': 'You dont have the rights to modify this delegation.'}, 403


@delegations_bp.route('/delegations/<delegation_id>', methods=['DELETE'])
@User.is_logged_in
def delete_delegation(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        try:
            delegation.delete()
            return 'Success.', 201
        except IntegrityError as e:
            sqlalchemy_session.rollback()
            return 'Fail.', 400
    return {'response': 'You dont have the rights to delete this delegation.'}, 403