from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from app.database.tables_declaration import *

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/delegations/<delegation_id>/settlements/<settlement_id>/expenses', methods=['GET'])
@User.is_logged_in
@Delegation.if_exists
@Settlement.if_exists
@Settlement.is_correct_child
def expenses_list_view(delegation_id, settlement_id):
    delegation = Delegation.get_by_id(delegation_id)
    settlement = Settlement.get_by_id(settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        expenses_list = settlement.expense
        expenses_list = [expense.show() for expense in expenses_list]
        return jsonify(expenses_list), 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@expenses_bp.route('/delegations/<delegation_id>/settlements/<settlement_id>/expenses', methods=['POST'])
@User.is_logged_in
@Delegation.if_exists
@Settlement.if_exists
@Settlement.is_correct_child
def add_expense(delegation_id, settlement_id):
    delegation = Delegation.get_by_id(delegation_id)
    settlement = Settlement.get_by_id(settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    expense_details = request.get_json()
    expense_details['settlement_id'] = settlement.id
    if user.is_authorized(delegation):
        try:
            Expense.create(expense_details)
            return 'Success.', 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return 'Fail.', 404
    return {'response': 'You dont have the rights to see this delegation.'}, 403


# @settlements_bp.route('/delegations/<delegation_id>/settlements/<settlement_id>', methods=['GET'])
# @User.is_logged_in
# @Delegation.if_exists
# @Settlement.if_exists
# @Settlement.is_correct_child
# def show_settlement(delegation_id, settlement_id):
#     delegation = Delegation.get_by_id(delegation_id)
#     settlement = Settlement.get_by_id(settlement_id)
#     user = User.get_by_token(request.headers.get('token'))
#     if user.is_authorized(delegation):
#         return jsonify(settlement.details()), 200
#     return {'response': 'You dont have the rights to see this delegation.'}, 403
#
#
# @settlements_bp.route('/delegations/<delegation_id>/settlements/<settlement_id>', methods=['PUT'])
# @User.is_logged_in
# @Delegation.if_exists
# @Settlement.if_exists
# @Settlement.is_correct_child
# def modify_settlement(delegation_id, settlement_id):
#     delegation = Delegation.get_by_id(delegation_id)
#     settlement = Settlement.get_by_id(settlement_id)
#     body = request.get_json()
#     user = User.get_by_token(request.headers.get('token'))
#     if user.is_authorized(delegation):
#         try:
#             settlement.modify(body)
#             return 'Success.', 201
#         except InvalidRequestError:
#             return 'Fail.', 400
#     return {'response': 'You dont have the rights to see this delegation.'}, 403
#
#
# @settlements_bp.route('/delegations/<delegation_id>/settlements/<settlement_id>', methods=['DELETE'])
# @User.is_logged_in
# @Delegation.if_exists
# @Settlement.if_exists
# @Settlement.is_correct_child
# def delete_settlement(delegation_id, settlement_id):
#     delegation = Delegation.get_by_id(delegation_id)
#     settlement = Settlement.get_by_id(settlement_id)
#     user = User.get_by_token(request.headers.get('token'))
#     if user.is_authorized(delegation):
#         try:
#             settlement.delete()
#             return 'Success.', 201
#         except InvalidRequestError:
#             return 'Fail.', 400
#     return {'response': 'You dont have the rights to see this delegation.'}, 403
