import pandas
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint, jsonify, request
from shortuuid import uuid
from app.database.tables_declaration import *


user_panel = Blueprint('user_panel', __name__)


@user_panel.route('/countries', methods=['GET'])
def get_countries_list():
    countries_and_rates = pandas.read_csv('foreign_diet_rate.csv', delimiter=';')
    countries_list = countries_and_rates['Country'].to_list()
    return jsonify(countries_list)


@user_panel.route('/user_panel', methods=['GET'])
@User.is_logged_in
def user_panel_view():
    user = User.get_user_by_token(request.headers.get('token'))
    delegations = user.get_user_delegations()
    delegations = [str(delegation) for delegation in delegations]
    return jsonify(delegations)


@user_panel.route('/user_panel', methods=['POST'])
@User.is_logged_in
def add_delegation_request():
    user = User.get_user_by_token(request.headers.get('token'))
    # delegation_details = request.get_json()
    delegation_details = {'title': 'jakistitle',
                          'id': uuid(),
                          'maker_id': user.id}
    try:
        delegation_to_add = Delegation(**delegation_details)
        sqlalchemy_session.add(delegation_to_add)
        sqlalchemy_session.commit()
        return 'Success'
    except IntegrityError:
        sqlalchemy_session.rollback()
        return 'Delegation with same ID already exists.'


@user_panel.route('/modify_delegation', methods=['GET'])
@User.is_logged_in
def show_delegation():
    # delegation_details = request.get_json()
    delegation_details = {'id': '3VCL9nvJfedn7n3RegBPVE'}
    delegation_to_show = Delegation.get_delegation_by_id(delegation_details['id'])
    return str(delegation_to_show)


@user_panel.route('/modify_delegation', methods=['PUT'])
@User.is_logged_in
def modify_delegation():
    # delegation_details = request.get_json()
    delegation_details = {'id': '3VCL9nvJfedn7n3RegBPVE'}
    # modifications_dict = request.get_json()
    modifications_dict = {'title': 'changed again',
                          'worker_id': '63fBoF58UX2CaV7XusfaAf'}
    try:
        Delegation.modify_delegation(delegation_details, modifications_dict)
        return 'success'
    except InvalidRequestError:
        return 'fail'


@user_panel.route('/x')
def get_delegation():
    user_token = request.args.get("token")
    user = User.get_user_by_token(user_token)
    return jsonify(user)
