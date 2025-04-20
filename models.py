from werkzeug.security import check_password_hash, generate_password_hash
# from uuid import UUID

from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id: int, name: str, email: str, password: str, is_admin: bool = False) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def get_id(self) -> str:
        return str(self.user_id)

    def __repr__(self) -> str:
        return f"<class User(email={self.email})>"


users = []


def get_user(email: str) -> User | None:
    for user in users:
        if user.email == email:
            return user

    return None
