from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.database.tables_declaration import *

attachments_bp = Blueprint('attachments', __name__)


@attachments_bp.route('/expenses/<expense_id>/attachments', methods=['GET'])
@User.is_logged_in
@Expense.if_exists
def attachments_list_view(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        attachments_list = expense.attachment
        attachments_list = [attachment.show() for attachment in attachments_list]
        return {'response': attachments_list}, 200
    return {'response': 'You dont have the rights to see this attachments.'}, 403


@attachments_bp.route('/expenses/<expense_id>/attachments', methods=['POST'])
@User.is_logged_in
@Expense.if_exists
@Attachment.not_valid_dict
def add_attachment(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    attachment_details = request.get_json()
    attachment_details['expense_id'] = expense.id
    if user.is_authorized(settlement):
        try:
            new_attachment = Attachment.create(attachment_details)
            return {'response': new_attachment.show()}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to create this attachment.'}, 403


@attachments_bp.route('/attachments/<attachment_id>', methods=['GET'])
@User.is_logged_in
@Attachment.if_exists
def show_attachment(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': attachment.show()}, 200
    return {'response': 'You dont have the rights to see this attachment.'}, 403


@attachments_bp.route('/attachments/<attachment_id>', methods=['PUT'])
@User.is_logged_in
@Attachment.if_exists
@Attachment.not_valid_dict
def modify_attachment(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    attachment_details = request.get_json()
    if user.is_authorized(settlement):
        try:
            attachment.modify(attachment_details)
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this attachment.'}, 403


@attachments_bp.route('/attachments/<attachment_id>', methods=['DELETE'])
@User.is_logged_in
@Attachment.if_exists
def delete_expense(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            attachment.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this attachment.'}, 403
