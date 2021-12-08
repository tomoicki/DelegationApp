from flask import Blueprint
from app.database.tables_declaration import *

admin = Blueprint("admin", __name__)


@admin.route("/admin/all_settlements/<country>", methods=["GET"])
@admin.route("/admin/all_settlements", methods=["GET"])
def all_settlements(country=None):
    settlements = sqlalchemy_session.query(Settlement).all()
    cntry, d_email, st = "country", "delegate_email", "settlement_id"
    if country is None:
        result = [{cntry: s.show()["country"], d_email: s.show()["delegate_email"], st: s.id} for s in settlements]
        return {"response": result}, 200
    else:
        result = [
            {cntry: s.show()["country"], d_email: s.show()["delegate_email"], st: s.id} \
            for s in settlements if s.show()["country"] == country
        ]
        return {"response": result}, 200
