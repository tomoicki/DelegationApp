from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

settlements_bp = Blueprint('settlements', __name__)


@settlements_bp.route('/delegations/<delegation_id>/settlements', methods=['GET'])
@User.is_logged_in
@Delegation.if_exists
def settlement_list_view(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        settlements_list = delegation.settlement
        settlements_list = [settlement.show() for settlement in settlements_list]
        return jsonify(settlements_list), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/delegations/<delegation_id>/settlements', methods=['POST'])
@User.is_logged_in
@Delegation.if_exists
def add_settlement(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    settlement_details = request.get_json()
    settlement_details['delegation_id'] = delegation.id
    if user.is_authorized(delegation):
        if User.get_by_id(settlement_details['approver_id']) is None:
            return {'response': 'Cannot find user with provided "approver_id".'}, 404
        try:
            Settlement.create(settlement_details)
            return {'response': 'Success.'}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['GET'])
@User.is_logged_in
@Delegation.if_exists
@Settlement.if_exists
@Settlement.is_correct_child
def show_settlement(delegation_id, settlement_id):
    delegation = Delegation.get_by_id(delegation_id)
    settlement = Settlement.get_by_id(settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        return jsonify(settlement.details()), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['PUT'])
@User.is_logged_in
@Delegation.if_exists
@Settlement.if_exists
@Settlement.is_correct_child
def modify_settlement(delegation_id, settlement_id):
    delegation = Delegation.get_by_id(delegation_id)
    settlement = Settlement.get_by_id(settlement_id)
    body = request.get_json()
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        try:
            settlement.modify(body)
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['DELETE'])
@User.is_logged_in
@Delegation.if_exists
@Settlement.if_exists
@Settlement.is_correct_child
def delete_settlement(delegation_id, settlement_id):
    delegation = Delegation.get_by_id(delegation_id)
    settlement = Settlement.get_by_id(settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        try:
            settlement.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403
