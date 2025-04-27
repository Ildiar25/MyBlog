from __future__ import annotations
import uuid
from datetime import datetime

from slugify import slugify
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from app import db


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
        return Post.query.filter_by(slug_title=slug).first()

    @staticmethod
    def get_all() -> list[Post]:
        return Post.query.all()

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
