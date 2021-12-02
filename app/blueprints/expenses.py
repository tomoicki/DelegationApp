from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from flask import Blueprint
from app.tools.useful_functions import id_from_str_to_int, amount_parser
from app.database.tables_declaration import *

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/settlements/<settlement_id>/expenses', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def expenses_list_view(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        response = settlement.give_sorted_expenses()
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
    if 'transit_type_id' in expense_details.keys() and expense_details['type'] != 'transit':
        return {'response': "'transit_type_id' key can only be added if 'type' is 'transit'. "}, 404
    if user.is_authorized(settlement):
        try:
            expense_details['settlement_id'] = settlement.id
            expense_details['amount'] = amount_parser(expense_details['amount'])
            expense_details = id_from_str_to_int(expense_details)
            new_expense = Expense.create(expense_details)
            response = settlement.give_sorted_expenses()
            return {'response': response}, 201
        except DataError:
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
    expense_details['amount'] = amount_parser(expense_details['amount'])
    if 'transit_type_id' in expense_details.keys() and expense_details['type'] != 'transit':
        return {'response': "'transit_type_id' key can only be added if 'type' is 'transit'. "}, 404
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
    print(settlement)
    user = Users.get_by_token(request.headers.get('token'))
    print(str(user))
    if user.is_authorized(settlement):
        try:
            expense.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to see this delegation.'}, 403
