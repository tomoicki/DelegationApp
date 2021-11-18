from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, send_from_directory
from app.tools.useful_functions import id_from_str_to_int
from app.database.tables_declaration import *

expense_attachments_bp = Blueprint('expense_attachments', __name__)


@expense_attachments_bp.route('/expenses/<expense_id>/attachments', methods=['GET'])
@Users.is_logged_in
@Expense.if_exists
def expense_attachments_list_view(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        attachments_list = expense.attachment
        attachments_list = [attachment.show() for attachment in attachments_list]
        return {'response': attachments_list}, 200
    return {'response': 'You dont have the rights to see this attachments.'}, 403


@expense_attachments_bp.route('/expenses/<expense_id>/attachments', methods=['POST'])
@Users.is_logged_in
@Expense.if_exists
@ExpenseAttachment.not_valid_dict
def add_expense_attachment(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            response = ExpenseAttachment.create(expense.id)
            return {'response': response}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to create this attachment.'}, 403


@expense_attachments_bp.route('/expense_attachments/<attachment_id>', methods=['GET'])
@Users.is_logged_in
@ExpenseAttachment.if_exists
def show_expense_attachment(attachment_id):
    attachment = ExpenseAttachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        expense_path = os.path.join(uploads_dir, 'expense_' + str(attachment.expense_id))
        return send_from_directory(expense_path, attachment.path.rsplit('\\', 1)[-1])
    return {'response': 'You dont have the rights to see this attachment.'}, 403


@expense_attachments_bp.route('/expense_attachments/<attachment_id>', methods=['PUT'])
@Users.is_logged_in
@ExpenseAttachment.if_exists
@ExpenseAttachment.not_valid_dict
def modify_expense_attachment(attachment_id):
    attachment = ExpenseAttachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    attachment_details = request.get_json()
    if user.is_authorized(settlement):
        try:
            modified_attachment = attachment.modify(attachment_details)
            return {'response': modified_attachment.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this attachment.'}, 403


@expense_attachments_bp.route('/expense_attachments/<attachment_id>', methods=['DELETE'])
@Users.is_logged_in
@ExpenseAttachment.if_exists
def delete_expense_expense(attachment_id):
    attachment = ExpenseAttachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            attachment.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this attachment.'}, 403
