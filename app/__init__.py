import os
from enum import Enum
from logging import DEBUG, ERROR, Formatter, Handler, INFO, StreamHandler
from logging.handlers import SMTPHandler

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized

from .common.filters import give_format_to_date


class AppConfig(Enum):
    DEV = "development.py"
    PROD = "production.py"
    TEST = "testing.py"
    DEFAULT = "default.py"


def __register_filters(app: Flask) -> None:
    app.jinja_env.filters['datetime'] = give_format_to_date


def __register_errors_handler(app: Flask) -> None:

    @app.errorhandler(401)
    def unauthorized(_: Unauthorized) -> tuple[str, int]:
        return render_template("unauthorized.html"), 401

    @app.errorhandler(404)
    def not_found_error(_: NotFound) -> tuple[str, int]:
        return render_template("not_found.html"), 404

    @app.errorhandler(500)
    def internal_server_error(_: InternalServerError) -> tuple[str, int]:
        return render_template("internal_server_error.html"), 500


def __logger_settings(app: Flask) -> None:
    # Clear all previous handlers
    app.logger.handlers.clear()

    # Set default loggers & handlers
    loggers = [app.logger, ]
    handlers = []

    # Terminal handler
    console_handler = __set_handler_level(StreamHandler(), app)
    console_handler.setFormatter(__set_format_string())
    handlers.append(console_handler)

    # Mail handler
    if app.config["APP_ENV"] == "production":
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_HOST"], app.config["MAIL_PORT"]),
            fromaddr=app.config["DONT_REPLY_FROM"],
            toaddrs=app.config["ADMINS"],
            subject=f"[Error][{app.config['APP_ENV']}] La aplicación falló",
            # credentials=(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        )
        mail_handler.setLevel(ERROR)
        mail_handler.setFormatter(__set_email_format_string())
        handlers.append(mail_handler)

    for log in loggers:
        for handler in handlers:
            log.addHandler(handler)
        log.propagate = False
        log.setLevel(DEBUG)


def __set_handler_level(handler: Handler, app: Flask) -> Handler:
    if app.config["APP_ENV"] == "local" or app.config["APP_ENV"] == "development" or app.config["APP_ENV"] == "testing":
        handler.setLevel(DEBUG)
    else:
        handler.setLevel(INFO)

    return handler


def __set_format_string() -> Formatter:
    return Formatter(
        fmt="[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )


def __set_email_format_string() -> Formatter:
    return Formatter(
        fmt="""
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s.%(msecs)d
        
        Message:
        %(message)s
        """,
        datefmt="%d/%m/%Y %H:%M:%S"
    )


def create_app(config: AppConfig) -> Flask:
    app = Flask(__name__)
    app_config = os.path.join(os.getcwd(), "config", config.value)
    app.config.from_pyfile(app_config)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    # Set logging
    __logger_settings(app)

    # Init migration
    migrate.init_app(app, db)

    # Init mail
    mail.init_app(app)

    # Add filters
    __register_filters(app)

    # noinspection PyPep8
    from .admin import admin
    app.register_blueprint(admin)

    # noinspection PyPep8
    from .auth import auth
    app.register_blueprint(auth)

    # noinspection PyPep8
    from .profile import profile
    app.register_blueprint(profile)

    # noinspection PyPep8
    from .public import public
    app.register_blueprint(public)

    # Error handlers
    __register_errors_handler(app)

    return app


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
