import os
from flask import Flask, Blueprint
from .models import db


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'config')

    db.init_app(app)

    if (app.config['DEBUG']):
        angular = Blueprint('angular', __name__, static_url_path='', static_folder='../../client')
        @app.route('/')
        def root():
            return angular.send_static_file('index.html')
        app.register_blueprint(angular)

    from api.v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    from api.v1_0.administrador import api as administracao_blueprint
    app.register_blueprint(administracao_blueprint, url_prefix='/api/v1.0')

    if app.config['USE_TOKEN_AUTH']:
        from api.token import token as token_blueprint
        app.register_blueprint(token_blueprint, url_prefix='/auth')
    return app
