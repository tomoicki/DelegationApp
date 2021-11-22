from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from flask import Blueprint
from app.tools.useful_functions import id_from_str_to_int, amount_parser
from app.database.tables_declaration import *

advance_payments_bp = Blueprint('advance_payments', __name__)


@advance_payments_bp.route('/settlements/<settlement_id>/advance_payments', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def advance_payments_list_view(settlement_id):
    user = Users.get_by_token(request.headers.get('token'))
    settlement = Settlement.get_by_id(settlement_id)
    if user.is_authorized(settlement):
        advance_payments_list = settlement.advance_payment
        advance_payments_list = [advance_payment.show() for advance_payment in advance_payments_list]
        return {'response': advance_payments_list}, 200
    return {'response': 'You dont have the rights to see this advance payment list.'}, 403


@advance_payments_bp.route('/settlements/<settlement_id>/advance_payments', methods=['POST'])
@Users.is_logged_in
@Settlement.if_exists
@AdvancePayment.not_valid_dict
def add_advance_payment(settlement_id):
    creator = Users.get_by_token(request.headers.get('token'))
    settlement = Settlement.get_by_id(settlement_id)
    advance_payment_details_list = request.get_json()
    if not creator.id == settlement.delegate_id and creator.role.value not in ['manager', 'hr', 'admin']:
        return {'response': 'You dont have the rights to create this delegation.'}, 403
    try:
        response = []
        for advance_payment_details in advance_payment_details_list:
            advance_payment_details['settlement_id'] = settlement.id
            advance_payment_details['submit_date'] = datetime.datetime.now()
            advance_payment_details = id_from_str_to_int(advance_payment_details)
            advance_payment_details['amount'] = amount_parser(advance_payment_details['amount'])
            new_delegation = AdvancePayment.create(advance_payment_details)
            response.append(new_delegation.show())
        return {'response': response}, 201
    except DataError:
        sqlalchemy_session.rollback()
        return {'response': 'Fail.'}, 404


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['GET'])
@Users.is_logged_in
@AdvancePayment.if_exists
def show_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    settlement = Settlement.get_by_id(advance_payment.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': advance_payment.show()}, 200
    return {'response': 'You dont have the rights to see this advance payment.'}, 403


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['PUT'])
@Users.is_logged_in
@AdvancePayment.if_exists
@AdvancePayment.not_valid_dict
def modify_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    settlement = Settlement.get_by_id(advance_payment.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    advance_payment_details = id_from_str_to_int(request.get_json())
    if user.is_authorized(settlement):
        try:
            modified_advance_payment = advance_payment.modify(advance_payment_details)
            return {'response': modified_advance_payment.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this advance payment.'}, 403


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['DELETE'])
@Users.is_logged_in
@AdvancePayment.if_exists
def delete_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    settlement = Settlement.get_by_id(advance_payment.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            advance_payment.delete()
            return {'response': 'Success.'}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this advance payment.'}, 403
