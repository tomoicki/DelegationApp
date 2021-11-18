from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask import Blueprint
from app.tools.useful_functions import id_from_str_to_int
from app.database.tables_declaration import *

provision_attachments_bp = Blueprint('provision_attachments', __name__)


@provision_attachments_bp.route('/provisions/<provision_id>/attachments', methods=['GET'])
@Users.is_logged_in
@Provision.if_exists
def provision_attachments_list_view(provision_id):
    provision = Provision.get_by_id(provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        attachments_list = provision.attachment
        attachments_list = [attachment.show() for attachment in attachments_list]
        return {'response': attachments_list}, 200
    return {'response': 'You dont have the rights to see this attachments.'}, 403


@provision_attachments_bp.route('/provisions/<provision_id>/attachments', methods=['POST'])
@Users.is_logged_in
@Provision.if_exists
@ProvisionAttachment.not_valid_dict
def add_provision_attachment(provision_id):
    provision = Provision.get_by_id(provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            response = ProvisionAttachment.create(provision.id)
            return {'response': response}, 201
        except IntegrityError:
            sqlalchemy_session.rollback()
            return {'response': 'Fail.'}, 404
    return {'response': 'You dont have the rights to create this attachment.'}, 403


@provision_attachments_bp.route('/provision_attachments/<attachment_id>', methods=['GET'])
@Users.is_logged_in
@ProvisionAttachment.if_exists
def show_provision_attachment(attachment_id):
    attachment = ProvisionAttachment.get_by_id(attachment_id)
    provision = Provision.get_by_id(attachment.provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        return {'response': attachment.show()}, 200
    return {'response': 'You dont have the rights to see this attachment.'}, 403


@provision_attachments_bp.route('/provision_attachments/<attachment_id>', methods=['PUT'])
@Users.is_logged_in
@ProvisionAttachment.if_exists
@ProvisionAttachment.not_valid_dict
def modify_provision_attachment(attachment_id):
    attachment = ProvisionAttachment.get_by_id(attachment_id)
    provision = Provision.get_by_id(attachment.provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    attachment_details = request.get_json()
    if user.is_authorized(settlement):
        try:
            modified_attachment = attachment.modify(attachment_details)
            return {'response': modified_attachment.show()}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to modify this attachment.'}, 403


@provision_attachments_bp.route('/provision_attachments/<attachment_id>', methods=['DELETE'])
@Users.is_logged_in
@ProvisionAttachment.if_exists
def delete_provision_provision(attachment_id):
    attachment = ProvisionAttachment.get_by_id(attachment_id)
    provision = Provision.get_by_id(attachment.provision_id)
    settlement = Settlement.get_by_id(provision.settlement_id)
    user = Users.get_by_token(request.headers.get('token'))
    if user.is_authorized(settlement):
        try:
            attachment.delete()
            return {'response': 'Success.'}, 201
        except InvalidRequestError:
            return {'response': 'Fail.'}, 400
    return {'response': 'You dont have the rights to delete this attachment.'}, 403
