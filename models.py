from __future__ import annotations

from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
# from uuid import UUID
from flask_login import UserMixin

from run import db


class User(db.Model, UserMixin):

    __table_name__ = "blog_user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # def __init__(self, user_id: int, name: str, email: str, password: str, is_admin: bool = False) -> None:
    #     self.user_id = user_id
    #     self.name = name
    #     self.email = email
    #     self.password = generate_password_hash(password)
    #     self.is_admin = is_admin

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def save(self) -> None:
        if not self.user_id:
            db.session.add(self)

        db.session.commit()

    # This method overwrites UserMixin
    def get_id(self) -> str:
        return str(self.user_id)

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def __repr__(self) -> str:
        return f"<class User(email={self.email})>"


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("blog_user.user_id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    slug_title = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text())

    # def __init__(self, post_id: int, title: str, slug_title: str, content: str) -> None:
    #     self.post_id = post_id
    #     self.title = title
    #     self.slug_title = slug_title
    #     self.content = content

    def save(self) -> None:
        if not self.post_id:
            db.session.add(self)
        if not self.slug_title:
            self.slug_title = slugify(self.title)

        saved = False
        counter = 0

        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                counter += 1
                self.slug_title = f'{slugify(self.title)}-{counter}'

    def public_url(self) -> str:
        return url_for("show_post", slug=self.slug_title)

    @staticmethod
    def get_by_slug(slug: str) -> Post | None:
        return Post.query.filter_by(slug_title=slug).first()

    @staticmethod
    def get_all() -> list[Post]:
        return Post.query.all()

    def __repr__(self) -> str:
        return f"<class Post(title={self.title})>"
