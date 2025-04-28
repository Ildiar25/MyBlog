from typing import Final

# Development settings
DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///../instance/blog.db"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
ITEMS_PER_PAGE = 10
