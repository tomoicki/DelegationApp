from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from flask import Blueprint
from flask.helpers import send_file
from app.tools.useful_functions import id_from_str_to_int, amount_parser
from app.database.tables_declaration import *

settlements_bp = Blueprint('settlements', __name__)


@settlements_bp.route('/settlements/<settlement_id>/pdf', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def get_pdf(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        pdf = settlement.generate_pdf()
        pdf.seek(0)
        return send_file(pdf, as_attachment=True, mimetype='application/pdf',
                         attachment_filename=f'settlement_{settlement_id}.pdf', cache_timeout=0)
    return {'response': 'You dont have the rights to see this pdf.'}, 403


@settlements_bp.route('/settlements', methods=['GET'])
@Users.is_logged_in
def settlement_list_view():
    user = Users.get_by_token(request.headers.get('token'))
    settlements_list = user.settlement_his
    settlements_list = [settlement.details() for settlement in settlements_list]
    return {'response': settlements_list}, 200


@settlements_bp.route('/settlements', methods=['POST'])
@Users.is_logged_in
@Settlement.not_valid_dict
def add_settlement():
    creator = Users.get_by_token(request.headers.get('token'))
    settlement_details = id_from_str_to_int(request.get_json())
    if not creator.id == settlement_details['delegate_id'] and creator.role.value not in ['manager', 'hr', 'admin']:
        return {'response': 'You dont have the rights to create this settlement.'}, 403
    if Users.get_by_id(settlement_details['approver_id']) is None:
        return {'response': 'Cannot find user with provided approver_id.'}, 404
    settlement_details['creator_id'] = creator.id
    try:
        new_settlement = Settlement.create(settlement_details)
        return {'response': new_settlement.details()}, 201
    except DataError:
        sqlalchemy_session.rollback()
        return {'response': 'Fail.'}, 404


@settlements_bp.route('/settlements/<settlement_id>', methods=['GET'])
@Users.is_logged_in
@Settlement.if_exists
def show_settlement(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        calculations = request.args.get("calculations", '')
        if calculations.lower() == 'true':
            sum_of_advanced_payments_by_currency = settlement.sum_of_advanced_payments()
            adv_in_pln = [d['amount'] for d in sum_of_advanced_payments_by_currency if d['currency_name'] == 'PLN']
            if not adv_in_pln:
                adv_in_pln.append(0)
            response_dict = {'sum_of_expenses_in_PLN': settlement.sum_of_expenses(),
                             'sum_of_advanced_payments_by_currency': sum_of_advanced_payments_by_currency,
                             'diets': settlement.calculate_diet()}
            compensation = float(response_dict['diets']['diet_meal_reduced']) + \
                           float(response_dict['sum_of_expenses_in_PLN']['total']) - \
                           float(adv_in_pln[0])
            response_dict['compensations'] = str(format(compensation, '.2f'))
            response_dict['sum_of_expenses_in_PLN']['compensations'] = str(format(compensation, '.2f'))
            return {"response": response_dict}, 200
        return {'response': settlement.details()}, 200
    return {'response': 'You dont have the rights to see this settlement.'}, 403


@settlements_bp.route('/settlements/<settlement_id>', methods=['PUT'])
@Users.is_logged_in
@Settlement.if_exists
@Settlement.not_valid_dict
def modify_settlement(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    settlement_details = id_from_str_to_int(request.get_json())
    if user.is_authorized(settlement):
        try:
            modified_settlement = settlement.modify(settlement_details)
            return {'response': modified_settlement.details()}, 201
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
