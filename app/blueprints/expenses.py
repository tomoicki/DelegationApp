from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.tools.useful_functions import id_from_str_to_int
from app.database.tables_declaration import *

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/settlements/<settlement_id>/expenses', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def expenses_list_view(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        expenses_list = settlement.expense
        expenses_list = [expense.show() for expense in expenses_list]
        currency_set = {expense['currency'] for expense in expenses_list}
        type_amount = {currency: {expense_type: str(sum([float(expense['amount']) for expense in expenses_list if
                                                         expense['currency'] == currency and expense['type'] == expense_type]))
                                  for expense_type in {expense['type'] for expense in expenses_list if
                                                       expense['currency'] == currency}} for currency in currency_set}
        total_amount = {currency: {'total': str(sum([float(expense['amount']) for expense in expenses_list if
                                                     expense['currency'] == currency])) for expense in expenses_list if
                                   expense['currency'] == currency} for currency in currency_set}
        response = [{'currency': currency,
                     'total_amount': total_amount[currency]['total'],
                     'type_amount': type_amount[currency],
                     'expenses': [expense for expense in expenses_list if expense['currency'] == currency]}
                    for currency in currency_set]
        return {'response': response}, 200
    return {'response': 'You dont have the rights to see this expenses.'}, 403


@expenses_bp.route('/settlements/<settlement_id>/expenses', methods=['POST'])
@Users.is_logged_in
@Settlement.if_exists
@Expense.not_valid_dict
def add_expense(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    expense_details = request.get_json()
    if user.is_authorized(settlement):
        try:
            expense_details['settlement_id'] = settlement.id
            expense_details = id_from_str_to_int(expense_details)
            new_expense = Expense.create(expense_details)
            return {'response': new_expense.show()}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to add this expense.'}, 403


@expenses_bp.route('/expenses/<expense_id>', methods=['GET'])
@Users.is_logged_in
@Expense.if_exists
def show_expense(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': expense.show()}, 200
    return {'response': 'You dont have the rights to see this expense.'}, 403


@expenses_bp.route('/expenses/<expense_id>', methods=['PUT'])
@Users.is_logged_in
@Expense.if_exists
@Expense.not_valid_dict
def modify_expense(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    expense_details = id_from_str_to_int(request.get_json())
    if user.is_authorized(settlement):
        try:
            modified_expense = expense.modify(expense_details)
            return {'response': modified_expense.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this expense.'}, 403


@expenses_bp.route('/expenses/<expense_id>', methods=['DELETE'])
@Users.is_logged_in
@Expense.if_exists
def delete_expense(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            expense.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403
