from pathlib import Path

from flask import current_app, render_template, redirect, request, Response, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.auth.models import User

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
        profile_pic = user.profile_pic

        if "profile_pic" in request.files:
            image = request.files["profile_pic"]

            if image.filename:
                profile_pic = secure_filename(image.filename)
                image_dir: Path = current_app.config["USER_MEDIA"]

                if not image_dir.exists():
                    image_dir.mkdir(parents=True, exist_ok=True)

                file_path = image_dir.joinpath(profile_pic)
                image.save(file_path)

        user.fullname = fullname
        user.profile_pic = profile_pic
        user.save()

        return redirect(url_for("profile.index"))

    return render_template(template_name_or_list="settings.html", form=form)
