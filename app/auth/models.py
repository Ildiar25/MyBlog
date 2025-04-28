from __future__ import annotations
import uuid
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model, UserMixin):
    """"""

    # Table settings
    __tablename__: str = "user"

    # Column settings
    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    fullname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    created: Mapped[datetime]
    modified: Mapped[datetime]
    last_login: Mapped[datetime | None]

    def __init__(self, fullname: str, email: str) -> None:
        self.fullname = fullname
        self.email = email

    @property
    def get_user_id(self) -> str:
        return self.user_id

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def update_last_login(self) -> None:
        self.last_login = datetime.now()

    def save(self) -> None:
        self.__update_user()
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # This method overrides UserMixin
    def get_id(self) -> str:
        return str(self.user_id)

    @staticmethod
    def get_by_user_id(user_id: str) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all() -> list[User]:
        return User.query.all()

    def __update_user(self) -> None:
        if not self.user_id:
            self.user_id = str(uuid.uuid4())
            db.session.add(self)

        if not self.created:
            self.created = datetime.now()

        self.modified = datetime.now()
