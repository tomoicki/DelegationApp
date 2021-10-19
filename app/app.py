from flask import Flask
from app.blueprints.login import login as login_blueprint
from app.blueprints.user_panel import user_panel as user_panel_blueprint
from app.blueprints.swagger import swagger_ui_blueprint, swagger_details
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'would like not to have this but apparently i have to'
    app.register_blueprint(login_blueprint)
    app.register_blueprint(user_panel_blueprint)
    app.register_blueprint(swagger_details)
    app.register_blueprint(swagger_ui_blueprint)
    return app
