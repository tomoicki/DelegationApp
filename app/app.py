from flask import Flask
from app.blueprints.login import login
from app.blueprints.dictionaries import dictionaries_bp
from app.blueprints.advance_payments import advance_payments_bp
from app.blueprints.settlements import settlements_bp
from app.blueprints.expenses import expenses_bp
from app.blueprints.expense_attachments import expense_attachments_bp
from app.blueprints.provisions import provisions_bp
from app.blueprints.provision_attachments import provision_attachments_bp
from app.blueprints.swagger import swagger_ui_blueprint, swagger_details
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'would like not to have this but apparently i have to'
    app.register_blueprint(login)
    app.register_blueprint(dictionaries_bp)
    app.register_blueprint(advance_payments_bp)
    app.register_blueprint(settlements_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(expense_attachments_bp)
    app.register_blueprint(provisions_bp)
    app.register_blueprint(provision_attachments_bp)
    app.register_blueprint(swagger_details)
    app.register_blueprint(swagger_ui_blueprint)
    return app
