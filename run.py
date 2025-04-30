from pathlib import Path

from flask import Response, send_from_directory

from app import AppConfig, create_app


app = create_app(AppConfig.DEV)


@app.route("/media/user_media/<string:profile_pic>")
def media_profile(profile_pic: str) -> Response:
    dir_path = app.config["USER_MEDIA"]
    return send_from_directory(dir_path, profile_pic)
