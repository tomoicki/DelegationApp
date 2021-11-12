from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.database.tables_declaration import *

delegations_bp = Blueprint('delegations', __name__)


@delegations_bp.route('/delegations', methods=['GET'])
@Users.is_logged_in
def delegations_list_view():
    user = Users.get_by_token(request.headers.get('token'))
    delegations_list = user.delegation_his
    delegations_list = [delegation.show() for delegation in delegations_list]
    return {'response': delegations_list}, 200


@delegations_bp.route('/delegations', methods=['POST'])
@Users.is_logged_in
def add_delegation():
    creator = Users.get_by_token(request.headers.get('token'))
    delegation_details = request.get_json()
    if not creator.id == delegation_details['delegate_id'] and creator.role.value not in ['manager', 'hr', 'admin']:
        return {'response': 'You dont have the rights to create this delegation.'}, 403
    if Users.get_by_id(delegation_details['approver_id']) is None:
        return {'response': 'Cannot find user with provided "approver_id".'}, 404
    delegation_details['creator_id'] = creator.id
    try:
        new_delegation = Delegation.create(delegation_details)
        return {'response': new_delegation.show()}, 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'Fail.'}, 404


@delegations_bp.route('/delegations/<delegation_id>', methods=['GET'])
@Users.is_logged_in
@Delegation.if_exists
def show_delegation(delegation_id):
    delegation = Delegation.get_by_id(delegation_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        delegation_details = delegation.show()
        return {'response': delegation_details}, 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@delegations_bp.route('/delegations/<delegation_id>', methods=['PUT'])
@Users.is_logged_in
@Delegation.if_exists
def modify_delegation(delegation_id):
    user = Users.get_by_token(request.headers.get('token'))
    body = request.get_json()
    delegation = Delegation.get_by_id(delegation_id)
    if user.is_authorized(delegation):
        try:
            delegation.modify(body)
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@delegations_bp.route('/delegations/<delegation_id>', methods=['DELETE'])
@Users.is_logged_in
@Delegation.if_exists
def delete_delegation(delegation_id):
    user = Users.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    if user.is_authorized(delegation):
        try:
            delegation.delete()
            return {'response': 'Success.'}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403
