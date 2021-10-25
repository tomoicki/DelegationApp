import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

settlements_bp = Blueprint('settlements', __name__)


@settlements_bp.route('/delegations/<delegation_id>/settlements', methods=['GET'])
@User.is_logged_in
def user_panel_view(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        settlements_list = delegation.settlement
        settlements_list = [settlement.details() for settlement in settlements_list]
        return {'response': settlements_list}, 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/delegations', methods=['POST'])
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


@settlements_bp.route('/delegations/<delegation_id>', methods=['GET'])
@User.is_logged_in
def show_delegation(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        return jsonify(delegation.details()), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/delegations/<delegation_id>', methods=['PUT'])
@User.is_logged_in
def modify_delegation(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    body = request.get_json()
    if delegation is None:
        return {'response': "Cannot find delegation with provided ID."}, 404
    if user.id == delegation.delegate_id or user.role.value in ['manager', 'hr', 'admin']:
        try:
            delegation.modify(body)
            return 'Success.', 201
        except InvalidRequestError:
            return 'Fail.', 400
    return {'response': 'You dont have the rights to modify this delegation.'}, 403


@settlements_bp.route('/delegations/<delegation_id>', methods=['DELETE'])
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
