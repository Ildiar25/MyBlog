from pathlib import Path
from typing import Final

# Define app directories
BASE_DIR: Path = Path(__file__).parent.parent
MEDIA_DIR: Path = BASE_DIR.joinpath("media")
USER_MEDIA: Path = MEDIA_DIR.joinpath("user_media")
POST_MEDIA: Path = MEDIA_DIR.joinpath("post_media")

# Default settings
DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = "default"

# Database settings
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

# App behaviour
ITEMS_PER_PAGE = 10

# Email settings

print(BASE_DIR)
print(MEDIA_DIR)
