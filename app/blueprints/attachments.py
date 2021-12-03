from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from flask import Blueprint, send_from_directory
from app.tools.useful_functions import id_from_str_to_int
from werkzeug.exceptions import NotFound
from app.database.tables_declaration import *

attachments_bp = Blueprint('attachments', __name__)


@attachments_bp.route('/expenses/<expense_id>/attachments', methods=['GET'])
@Users.is_logged_in
@Expense.if_exists
def attachments_list_view(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        attachments_list = expense.attachment
        attachments_list = [attachment.show() for attachment in attachments_list]
        return {'response': attachments_list}, 200
    return {'response': 'You dont have the rights to see this attachments.'}, 403


@attachments_bp.route('/expenses/<expense_id>/attachments', methods=['POST'])
@Users.is_logged_in
@Expense.if_exists
@Attachment.not_valid_dict
def add_attachment(expense_id):
    expense = Expense.get_by_id(expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            response = Attachment.create(expense.id)
            return response
        except DataError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to create this attachment.'}, 403


@attachments_bp.route('/attachments/<attachment_id>', methods=['GET'])
@Users.is_logged_in
@Attachment.if_exists
def show_attachment(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        if not os.path.exists(attachment.path):
            return {'response': f"Cannot find attachment with name = '{attachment.name}' and id = '{attachment.id}' "
                                f"under path = '{attachment.path}'."}
        # return {"response": f"{attachment.path}, {attachment.path.rsplit('/', 1)}"}
        dir_and_file = attachment.path.rsplit('/', 1)
        # try:
        return send_from_directory(dir_and_file[0], dir_and_file[1], as_attachment=True)
        # except NotFound:
        #     return {'response': f'Cannot find attachment with name = {attachment.name} and id = {attachment.id} '
        #                         f'under path={attachment.path}.'}
    return {'response': 'You dont have the rights to see this attachment.'}, 403


@attachments_bp.route('/attachments/<attachment_id>', methods=['PUT'])
@Users.is_logged_in
@Attachment.if_exists
@Attachment.not_valid_dict
def modify_attachment(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
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


@attachments_bp.route('/attachments/<attachment_id>', methods=['DELETE'])
@Users.is_logged_in
@Attachment.if_exists
def delete_expense(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    expense = Expense.get_by_id(attachment.expense_id)
    settlement = Settlement.get_by_id(expense.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        if not os.path.exists(attachment.path):
            return {'response': f"Cannot find attachment with name = '{attachment.name}' and id = '{attachment.id}' "
                                f"under path = '{attachment.path}'."}
        try:
            os.remove(attachment.path)
            attachment.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this attachment.'}, 403
