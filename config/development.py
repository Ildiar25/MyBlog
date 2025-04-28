from typing import Final

# Development settings
DEBUG: Final[bool] = True
SECRET_KEY: Final[str] = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///../instance/database.db"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
ITEMS_PER_PAGE = 10
