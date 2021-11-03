from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.database.tables_declaration import *

advance_payments_bp = Blueprint('advance_payments', __name__)


@advance_payments_bp.route('/delegations/<delegation_id>/advance_payments', methods=['GET'])
@User.is_logged_in
@Delegation.if_exists
def advance_payments_list_view(delegation_id):
    user = User.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    if user.is_authorized(delegation):
        advance_payments_list = delegation.advance_payment
        advance_payments_list = [advance_payment.show() for advance_payment in advance_payments_list]
        return {'response': advance_payments_list}, 200
    return {'response': 'You dont have the rights to see this advance payment list.'}, 403


@advance_payments_bp.route('/delegations/<delegation_id>/advance_payments', methods=['POST'])
@User.is_logged_in
@Delegation.if_exists
def add_advance_payment(delegation_id):
    creator = User.get_by_token(request.headers.get('token'))
    delegation = Delegation.get_by_id(delegation_id)
    advance_payment_details = request.get_json()
    advance_payment_details['delegation_id'] = delegation.id
    if not creator.id == delegation.delegate_id and creator.role.value not in ['manager', 'hr', 'admin']:
        return {'response': 'You dont have the rights to create this delegation.'}, 403
    try:
        new_delegation = AdvancePayment.create(advance_payment_details)
        return {'response': new_delegation.show()}, 201
    except IntegrityError:
        sqlalchemy_session.rollback()
        return {'response': 'Fail.'}, 404


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['GET'])
@User.is_logged_in
@AdvancePayment.if_exists
def show_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    delegation = Delegation.get_by_id(advance_payment.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        return {'response': advance_payment.show()}, 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['PUT'])
@User.is_logged_in
@AdvancePayment.if_exists
def modify_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    delegation = Delegation.get_by_id(advance_payment.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    body = request.get_json()
    if user.is_authorized(delegation):
        try:
            advance_payment.modify(body)
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this advance payment.'}, 403


@advance_payments_bp.route('/advance_payments/<advance_payment_id>', methods=['DELETE'])
@User.is_logged_in
@AdvancePayment.if_exists
def delete_advance_payment(advance_payment_id):
    advance_payment = AdvancePayment.get_by_id(advance_payment_id)
    delegation = Delegation.get_by_id(advance_payment.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        try:
            advance_payment.delete()
            return {'response': 'Success.'}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this advance payment.'}, 403
