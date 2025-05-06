from pathlib import Path

from flask import current_app, render_template, redirect, request, Response, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import FileStorage

from app.auth.models import User
from app.common.image_tools import AvatarImage

from . import profile
from .forms import ProfileForm


@profile.route("/profile/")
@login_required
def index() -> str:
    return render_template(template_name_or_list="profile_index.html")


@profile.route("/profile/settings/", methods=["GET", "POST"])
@login_required
def settings() -> Response | str:
    user = User.get_by_user_id(current_user.user_id)
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        fullname = form.fullname.data

        if "profile_pic" in request.files:
            file: FileStorage = request.files["profile_pic"]
            if file.filename:
                image = AvatarImage(file.stream).open().crop_image().with_size(current_app.config["AVATAR_MAX_SIZE"])
                image_dir: Path = current_app.config["USER_MEDIA"]

                if not image_dir.exists():
                    image_dir.mkdir(parents=True, exist_ok=True)

                image.save(image_dir)
                user.profile_pic = image.get_name()

        user.fullname = fullname
        user.save()

        return redirect(url_for("profile.index"))

    return render_template(template_name_or_list="settings.html", form=form)
