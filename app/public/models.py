from __future__ import annotations
import uuid
from datetime import datetime

from flask_sqlalchemy.pagination import Pagination
from slugify import slugify
from sqlalchemy import ForeignKey, select, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.auth.models import User


class Comment(db.Model):
    """"""

    # Table settings
    __tablename__: str = "comment"

    # Column settings
    comment_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(column="user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    post_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(column="post.post_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    # user_name: Mapped[str] = mapped_column(String(80), nullable=False)
    content: Mapped[str] = mapped_column(Text())
    created: Mapped[datetime]
    modified: Mapped[datetime]

    # Relationship
    post: Mapped[Post] = relationship(
        argument="Post",
        back_populates="comments"
    )

    # Initializer
    def __init__(self, content: str, user_id: str, post_id: str) -> None:
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def save(self) -> None:
        self.__update_comment()
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def get_user_name(self) -> str:
        statement = select(User.fullname).where(User.user_id == self.user_id)
        return db.session.scalar(statement)

    @staticmethod
    def get_by_post_id(post_id: str) -> list[Comment]:
        statement = select(Comment).where(Comment.post_id == post_id)
        return db.session.scalars(statement).all()

    def __repr__(self) -> str:
        return (
            f"<class Comment("
            f"comment_id={repr(self.post_id)}, "
            f"user_name={repr(self.user_name)}, "
            f"content={repr(self.content)}, "
            f"created={repr(self.created.strftime('%d-%m-%Y_%H:%M:%S'))}, "
            f"modified={repr(self.modified.strftime('%d-%m-%Y_%H:%M:%S'))}, "
            f")>"
        )

    def __update_comment(self):
        if not self.comment_id:
            self.comment_id = str(uuid.uuid4())
            db.session.add(self)

        if not self.created:
            self.created = datetime.now()

        self.modified = datetime.now()


class Post(db.Model):
    """"""

    # Table settings
    __tablename__: str = "post"

    # Column settings
    post_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(column="user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(256))
    slug_title: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text())
    created: Mapped[datetime]
    modified: Mapped[datetime]

    # Relationship
    comments: Mapped[list[Comment]] = relationship(
        argument="Comment",
        back_populates="post",
        order_by="asc(Comment.created)"
    )

    # Initializer
    def __init__(self, title: str, content: str, user_id: str) -> None:
        self.title = title
        self.content = content
        self.user_id = user_id

    @property
    def get_post_id(self) -> str:
        return self.post_id

    @property
    def get_user_id(self) -> str:
        return self.user_id

    def save(self) -> None:
        self.__update_post()

        saved = False
        counter = 0

        while not saved:
            try:
                db.session.commit()
                saved = True

            except IntegrityError:
                # Sets new title slug
                counter += 1
                self.slug_title = f"{slugify(self.title)}-{counter}"

                # Cleans session error
                db.session.rollback()

                # Adds object to session again
                db.session.add(self)

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug: str) -> Post | None:
        statement = select(Post).where(Post.slug_title == slug)
        return db.session.scalars(statement).first()

    @staticmethod
    def get_all() -> list[Post]:
        statement = select(Post)
        return db.session.scalars(statement).all()

    @staticmethod
    def all_paginated(page: int = 1, per_page: int = 20) -> Pagination:
        statement = select(Post).order_by(Post.created.asc())
        return db.paginate(statement, page=page, per_page=per_page)

    def __repr__(self) -> str:
        return (
            f"<class Post("
            f"post_id={repr(self.post_id)}, "
            f"title={repr(self.title)}, "
            f"slug_title={repr(self.slug_title)}, "
            f"content={repr(self.content)}, "
            f"created={repr(self.created.strftime('%d-%m-%Y_%H:%M:%S'))}, "
            f"modified={repr(self.modified.strftime('%d-%m-%Y_%H:%M:%S'))}, "
            f")>"
        )

    def __update_post(self) -> None:
        if not self.post_id:
            self.post_id = str(uuid.uuid4())
            db.session.add(self)

        if not self.slug_title:
            self.slug_title = slugify(self.title)

        if not self.created:
            self.created = datetime.now()

        self.modified = datetime.now()
