import unittest

from app import AppConfig, create_app, db
from app.auth.models import User


class UserBuilder:
    def __init__(self) -> None:
        self.__user = User(fullname="", email="")
        self.__user.set_password("Testing1234")

    def with_name(self, name: str) -> "UserBuilder":
        self.__user.fullname = name
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self.__user.email = email
        return self

    def is_admin(self) -> "UserBuilder":
        self.__user.is_admin = True
        return self

    def build(self) -> User:
        return self.__user


class BaseTestClass(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(AppConfig.TEST)
        self.client = self.app.test_client()
        self.user_admin = UserBuilder().with_name("Admin").with_email("admin@email.com").is_admin().build()
        self.user_client = UserBuilder().with_name("Client").with_email("client@email.com").build()

        # Main ID's
        self.admin_id = None
        self.client_id = None

        # Create app context
        with self.app.app_context():
            db.create_all()
            self.user_admin.save()
            self.user_client.save()

            self.admin_id = self.user_admin.user_id
            self.client_id = self.user_client.user_id

    def tearDown(self) -> None:
        with self.app.app_context():
            db.session.remove()

            # Delete all tables
            db.drop_all()
