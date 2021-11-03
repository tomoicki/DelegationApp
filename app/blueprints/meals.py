from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.database.tables_declaration import *

meals_bp = Blueprint('meals', __name__)


@meals_bp.route('/settlements/<settlement_id>/meals', methods=['GET'])
@User.is_logged_in
@Settlement.if_exists
def meals_list_view(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    delegation = Delegation.get_by_id(settlement.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        meals_list = settlement.meal
        meals_list = [meal.show() for meal in meals_list]
        return {'response': meals_list}, 200
    return {'response': 'You dont have the rights to see this meals.'}, 403


@meals_bp.route('/settlements/<settlement_id>/meals', methods=['POST'])
@User.is_logged_in
@Settlement.if_exists
def add_meal(settlement_id):
    settlement = Settlement.get_by_id(settlement_id)
    delegation = Delegation.get_by_id(settlement.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    meals_list = request.get_json()
    meals_list['settlement_id'] = settlement.id
    if user.is_authorized(delegation):
        try:
            new_meal = Meal.create(meals_list)
            return {'response': new_meal.show()}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to add this meal.'}, 403


@meals_bp.route('/meals/<meal_id>', methods=['GET'])
@User.is_logged_in
@Meal.if_exists
def show_meal(meal_id):
    meal = Meal.get_by_id(meal_id)
    settlement = Settlement.get_by_id(meal.settlement_id)
    delegation = Delegation.get_by_id(settlement.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        return {'response': meal.show()}, 200
    return {'response': 'You dont have the rights to see this delegation.'}, 403


@meals_bp.route('/meals/<meal_id>', methods=['PUT'])
@User.is_logged_in
@Meal.if_exists
def modify_meal(meal_id):
    meal = Meal.get_by_id(meal_id)
    settlement = Settlement.get_by_id(meal.settlement_id)
    delegation = Delegation.get_by_id(settlement.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    body = request.get_json()
    if user.is_authorized(delegation):
        try:
            meal.modify(body)
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this meal.'}, 403


@meals_bp.route('/meals/<meal_id>', methods=['DELETE'])
@User.is_logged_in
@Meal.if_exists
def delete_meal(meal_id):
    meal = Meal.get_by_id(meal_id)
    settlement = Settlement.get_by_id(meal.settlement_id)
    delegation = Delegation.get_by_id(settlement.delegation_id)
    user = User.get_by_token(request.headers.get('token'))
    if user.is_authorized(delegation):
        try:
            meal.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this meal.'}, 403
