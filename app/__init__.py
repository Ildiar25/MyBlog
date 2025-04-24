import os
from enum import Enum

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


class AppConfig(Enum):
    DEV = "development.py"
    PROD = "production.py"
    TEST = "testing.py"
    DEFAULT = "default.py"


login_manager = LoginManager()
db = SQLAlchemy()


def create_app(config: AppConfig = AppConfig.DEFAULT) -> Flask:
    app = Flask(__name__)
    app_config = os.path.join(os.getcwd(), "config", config.value)
    print(app_config)
    app.config.from_pyfile(app_config)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    # noinspection PyPep8
    from .public import public
    app.register_blueprint(public)

    # noinspection PyPep8
    from .auth import auth
    app.register_blueprint(auth)

    # noinspection PyPep8
    from .admin import admin
    app.register_blueprint(admin)

    return app
