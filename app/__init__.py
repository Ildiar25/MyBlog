from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../instance/database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
