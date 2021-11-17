from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.database.tables_declaration import *

settlements_bp = Blueprint('settlements', __name__)


@settlements_bp.route('/settlements', methods=['GET'])
@Users.is_logged_in
def settlement_list_view():
    user = Users.get_by_token(request.headers.get('token'))
    settlements_list = user.settlement_his
    settlements_list = [settlement.show() for settlement in settlements_list]
    return {'response': settlements_list}, 200


@settlements_bp.route('/settlements', methods=['POST'])
@Users.is_logged_in
@Settlement.not_valid_dict
def add_settlement():
    creator = Users.get_by_token(request.headers.get('token'))
    settlement_details = request.get_json()
    if not creator.id == settlement_details['delegate_id'] and creator.role.value not in ['manager', 'hr', 'admin']:
        return {'response': 'You dont have the rights to create this settlement.'}, 403
    if Users.get_by_id(settlement_details['approver_id']) is None:
        return {'response': 'Cannot find user with provided approver_id.'}, 404
    settlement_details['creator_id'] = creator.id
    try:
        new_settlement = Settlement.create(settlement_details)
        return {'response': new_settlement.details()}, 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'Fail.'}, 404


@settlements_bp.route('/settlements/<settlement_id>', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def show_settlement(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': settlement.details()}, 200
    return {'response': 'You dont have the rights to see this settlement.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['PUT'])
@Users.is_logged_in
@Settlement.if_exists
@Settlement.not_valid_dict
def modify_settlement(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    settlement_details = request.get_json()
    if user.is_authorized(settlement):
        try:
            modified_settlement = settlement.modify(settlement_details)
            return {'response': modified_settlement.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this settlement.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['DELETE'])
@Users.is_logged_in
@Settlement.if_exists
def delete_settlement(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            settlement.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this settlement.'}, 403
