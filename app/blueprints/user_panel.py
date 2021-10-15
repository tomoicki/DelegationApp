from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from shortuuid import uuid
from app.database.create_connection import sqlalchemy_session
from app.database.tables_declaration import *
from app.blueprints.login import is_logged_in, get_user_by_token

user_panel = Blueprint('user_panel', __name__, template_folder='Templates')


@user_panel.route('/user_panel', methods=['GET'])
@is_logged_in
def user_panel_view():
    user = get_user_by_token(request.headers.get('token'))
    delegations = sqlalchemy_session.query(Delegation).filter(Delegation.worker_id == user.id).all()
    delegations = [str(delegation) for delegation in delegations]
    return jsonify(delegations)


@user_panel.route('/user_panel', methods=['POST'])
@is_logged_in
def add_delegation_request():
    user = get_user_by_token(request.headers.get('token'))
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
