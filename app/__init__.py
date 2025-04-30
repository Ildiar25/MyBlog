import os
from enum import Enum

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized

from .common.filters import format_datetime

class AppConfig(Enum):
    DEV = "development.py"
    PROD = "production.py"
    TEST = "testing.py"
    DEFAULT = "default.py"


def register_filters(app: Flask) -> None:
    app.jinja_env.filters['datetime'] = format_datetime


def register_errors_handler(app: Flask) -> None:

    @app.errorhandler(401)
    def unauthorized(_: Unauthorized) -> tuple[str, int]:
        return render_template("unauthorized.html"), 401

    @app.errorhandler(404)
    def not_found_error(_: NotFound) -> tuple[str, int]:
        return render_template("not_found.html"), 404

    @app.errorhandler(500)
    def internal_server_error(_: InternalServerError) -> tuple[str, int]:
        return render_template("internal_server_error.html"), 500


def create_app(config: AppConfig) -> Flask:
    app = Flask(__name__)
    app_config = os.path.join(os.getcwd(), "config", config.value)
    app.config.from_pyfile(app_config)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    # Init migration
    migrate.init_app(app, db)

    # Add filters
    register_filters(app)

    # noinspection PyPep8
    from .public import public
    app.register_blueprint(public)

    # noinspection PyPep8
    from .auth import auth
    app.register_blueprint(auth)

    # noinspection PyPep8
    from .admin import admin
    app.register_blueprint(admin)

    # Error handlers
    register_errors_handler(app)

    return app


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
