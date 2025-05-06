from pathlib import Path
from typing import Final

# Define app directories
BASE_DIR: Final[Path] = Path(__file__).parent.parent
MEDIA_DIR: Final[Path] = BASE_DIR.joinpath("media")
USER_MEDIA: Final[Path] = MEDIA_DIR.joinpath("user_media")
POST_MEDIA: Final[Path] = MEDIA_DIR.joinpath("post_media")

# Production settings
DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
APP_ENV: Final[str] = "production"

# Database settings
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///../instance/blog.db"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

# App behaviour
ITEMS_PER_PAGE = 10

# Image Settings
AVATAR_MAX_SIZE: Final[tuple[int, int]] = (128, 128)

# Email settings
MAIL_HOST: Final[str] = "SMTP Server"
MAIL_PORT: Final[int] = 587
MAIL_USERNAME: Final[str] = "Your Email"
MAIL_PASSWORD: Final[str] = "Your Password"
DONT_REPLY_FROM: Final[str] = "An Email"
WEB_OWNER: Final[str] = "Owner Mail"
ADMINS: Final[tuple[str]] = ("Owner Mail", )
MAIL_USE_TLS: Final[bool] = True
MAIL_DEBUG: Final[bool] = False
