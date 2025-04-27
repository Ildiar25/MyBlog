from flask import abort, redirect, render_template, Response, url_for
from flask_login import current_user, login_required

from app.auth.decorators import admin_required
from app.public.models import Post

from . import admin
from .forms import PostForm


@admin.route("/admin/posts/", methods=["GET", "POST"])
@login_required
@admin_required
def create_post() -> Response | str:
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title=title, content=content, user_id=current_user.user_id)
        new_post.save()

        return redirect(url_for("public.index"))

    return render_template(template_name_or_list="create_post.html", form=form)


@admin.route("/admin/posts/<string:slug>/", methods=["GET", "POST"])
@login_required
@admin_required
def update_post(slug: str) -> Response | str:
    post = Post.get_by_slug(slug)

    if post is None:
        abort(404)
