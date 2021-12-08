from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from flask import Blueprint, send_from_directory
from app.tools.useful_functions import id_from_str_to_int
from werkzeug.exceptions import NotFound
from app.database.tables_declaration import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/all_settlements', methods=['GET'])
def show_delegation_to_country():
    all_settlements = sqlalchemy_session.query(Settlement).all()
    settlements_to_show = [settlement.admin_show() for settlement in all_settlements]
    country_filter = request.args.get("country_filter", False)
    if country_filter:
        settlements_to_show = [settlement for settlement in settlements_to_show if settlement['country'] == country_filter]
    return {'response': settlements_to_show}
