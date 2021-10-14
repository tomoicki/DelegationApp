from flask import Flask
from app.blueprints.login import login as login_blueprint


def create_app():
    app = Flask(__name__, template_folder='Templates')
    app.config['SECRET_KEY'] = 'would like not to have this but apparently i have to'
    app.register_blueprint(login_blueprint)
    return app
