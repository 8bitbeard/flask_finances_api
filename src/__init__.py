import os

from flask import Flask
from flask.json import jsonify

from flask_jwt_extended import JWTManager

from src.database import db, migrate, ma

from src.controllers.authentication_controller import auth
from src.controllers.users_controller import users
from src.controllers.accounts_controller import accounts
from src.controllers.transactions_controller import transactions
from src.controllers.categories_controller import categories

from src.constants import http_status_codes

from src.config import config_by_name

from src.exceptions.categories_exception import APIError


basedir = os.path.abspath(os.path.dirname(__file__))
MIGRATION_DIR = os.path.join(basedir, 'database', 'migrations')


def create_app(config_name='development'):

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['JSON_SORT_KEYS'] = False

    app.app_context().push()
    db.app=app
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)
    ma.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(accounts)
    app.register_blueprint(transactions)
    app.register_blueprint(categories)

    @app.errorhandler(http_status_codes.HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': 'Not found'
        }), http_status_codes.HTTP_404_NOT_FOUND

    @app.errorhandler(http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': 'Something went very very VERYY bad! We are working on it!!!'
        }), http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(APIError)
    def handle_exception(err):
        """Return custom JSON when APIError or its children are raised"""
        response = {
            "code": err.code,
            "message": "",
            "details": [
                err.details
            ]
        }
        if len(err.args) > 0:
            response["message"] = err.args[0]
        return jsonify(response), err.status_code

    return app
