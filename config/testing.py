from typing import Final

# Testing settings
DEBUG: Final[bool] = True
TESTING: Final[bool] = True
SECRET_KEY: Final[str] = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = True
ITEMS_PER_PAGE = 10
