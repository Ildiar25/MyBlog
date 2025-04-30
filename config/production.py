from pathlib import Path
from typing import Final

# Define app directories
BASE_DIR: Path = Path(__file__).parent.parent
MEDIA_DIR: Path = BASE_DIR.joinpath("media")
USER_MEDIA: Path = MEDIA_DIR.joinpath("user_media")
POST_MEDIA: Path = MEDIA_DIR.joinpath("post_media")

# Production settings
DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"

# Database settings
SQLALCHEMY_DATABASE_URI: Final[str] = "sqlite:///../instance/blog.db"
SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

# App behaviour
ITEMS_PER_PAGE = 10

# Email settings
