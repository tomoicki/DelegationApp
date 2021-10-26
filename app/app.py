from flask import Flask
from app.blueprints.login import login
from app.blueprints.lists import lists_bp
from app.blueprints.delegations import delegations_bp
from app.blueprints.settlements import settlements_bp
from app.blueprints.expenses import expenses_bp
from app.blueprints.swagger import swagger_ui_blueprint, swagger_details
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'would like not to have this but apparently i have to'
    app.register_blueprint(login)
    app.register_blueprint(lists_bp)
    app.register_blueprint(delegations_bp)
    app.register_blueprint(settlements_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(swagger_details)
    app.register_blueprint(swagger_ui_blueprint)
    return app
