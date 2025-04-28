from __future__ import annotations
import uuid
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import Boolean, select, String
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
        statement = select(User).where(User.user_id == user_id)
        return db.session.scalars(statement).first()

    @staticmethod
    def get_by_email(email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.session.scalars(statement).first()

    @staticmethod
    def get_all() -> list[User]:
        statement = select(User)
        return db.session.scalars(statement).all()

    @staticmethod
    def all_paginated(page: int = 1, per_page: int = 20) -> Pagination:
        statement = select(User).order_by(User.created.asc())
        return db.paginate(statement, page=page, per_page=per_page)

    def __update_user(self) -> None:
        if not self.user_id:
            self.user_id = str(uuid.uuid4())
            db.session.add(self)

        if not self.created:
            self.created = datetime.now()

        self.modified = datetime.now()
