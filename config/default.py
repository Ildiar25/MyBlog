from typing import Final

# Development settings
DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = "default"
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
ITEMS_PER_PAGE = 10
