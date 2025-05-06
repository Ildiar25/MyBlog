from pathlib import Path
from typing import Final

# Define app directories
BASE_DIR: Final[Path] = Path(__file__).parent.parent
MEDIA_DIR: Final[Path] = BASE_DIR.joinpath("media")
USER_MEDIA: Final[Path] = MEDIA_DIR.joinpath("user_media")
POST_MEDIA: Final[Path] = MEDIA_DIR.joinpath("post_media")

# Testing settings
DEBUG: Final[bool] = True
TESTING: Final[bool] = True
SECRET_KEY: Final[str] = "SECRET_KEY"
APP_ENV: Final[str] = "testing"

# Database settings
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = True

# App behaviour
ITEMS_PER_PAGE = 10

# Image Settings
AVATAR_MAX_SIZE: Final[tuple[int, int]] = (128, 128)

# Email settings
MAIL_HOST: Final[str] = "localhost"
MAIL_PORT: Final[int] = 1025
MAIL_USERNAME: Final[str] = ""
MAIL_PASSWORD: Final[str] = ""
DONT_REPLY_FROM: Final[str] = "app_email@example.com"
WEB_OWNER: Final[str] = "joan@gmail.com"
ADMINS: Final[tuple[str]] = ("joan@gmail.com", )
MAIL_USE_TLS: Final[bool] = True
MAIL_DEBUG: Final[bool] = False
