from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.tools.useful_functions import id_from_str_to_int
from app.database.tables_declaration import *

provisions_bp = Blueprint('provisions', __name__)


@provisions_bp.route('/settlements/<settlement_id>/provisions', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def provisions_list_view(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        provisions_list = settlement.provisions
        provisions_list = [provisions.show() for provisions in provisions_list]
        return {'response': provisions_list}, 200
    return {'response': 'You dont have the rights to see this provisions.'}, 403


@provisions_bp.route('/settlements/<settlement_id>/provisions', methods=['POST'])
@Users.is_logged_in
@Settlement.if_exists
@Provision.not_valid_dict
def add_provision(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    provision_details_list = request.get_json()
    if user.is_authorized(settlement):
        try:
            response = []
            for provision_details in provision_details_list:
                provision_details['settlement_id'] = settlement.id
                provision_details = id_from_str_to_int(provision_details)
                new_provision = Provision.create(provision_details)
                response.append(new_provision.show())
            return {'response': response}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to add this provision.'}, 403


@provisions_bp.route('/provisions/<provision_id>', methods=['GET'])
@Users.is_logged_in
@Provision.if_exists
def show_expense(provision_id):
    provision = Provision.get_by_id(provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': provision.show()}, 200
    return {'response': 'You dont have the rights to see this provision.'}, 403


@provisions_bp.route('/provisions/<provision_id>', methods=['PUT'])
@Users.is_logged_in
@Provision.if_exists
@Provision.not_valid_dict
def modify_expense(provision_id):
    provision = Provision.get_by_id(provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    expense_details = id_from_str_to_int(request.get_json())
    if user.is_authorized(settlement):
        try:
            modified_provision = provision.modify(expense_details)
            return {'response': modified_provision.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this provision.'}, 403


@provisions_bp.route('/provisions/<provision_id>', methods=['DELETE'])
@Users.is_logged_in
@Expense.if_exists
def delete_expense(provision_id):
    provision = Provision.get_by_id(provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            provision.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this provision.'}, 403
