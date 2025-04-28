from flask import abort, redirect, render_template, Response, url_for
from flask_login import current_user, login_required

from app.auth.decorators import admin_required
from app.auth.models import User
from app.public.models import Post

from . import admin
from .forms import PostForm, UserAdminForm


@admin.route("/admin/")
@login_required
@admin_required
def index() -> str:
    return render_template("admin_index.html")


@admin.route("/admin/posts/")
@login_required
@admin_required
def show_postlist() -> str:
    posts = Post.get_all()
    return render_template(template_name_or_list="posts.html", posts=posts)


@admin.route("/admin/new/", methods=["GET", "POST"])
@login_required
@admin_required
def create_post() -> Response | str:
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title=title, content=content, user_id=current_user.user_id)
        new_post.save()

        return redirect(url_for("admin.show_postlist"))

    return render_template(template_name_or_list="create_post.html", form=form)


@admin.route("/admin/posts/<string:slug>/", methods=["GET", "POST"])
@login_required
@admin_required
def update_post(slug: str) -> Response | str:
    post = Post.get_by_slug(slug)

    if not post:
        abort(404)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.save()

        return redirect(url_for("admin.show_postlist"))

    return render_template(template_name_or_list="create_post.html", form=form, post=post)


@admin.route("/admin/delete/<string:slug>/", methods=["GET", "POST"])
@login_required
@admin_required
def delete_post(slug: str) -> Response:
    post = Post.get_by_slug(slug)

    if not post:
        abort(404)

    post.delete()
    return redirect(url_for("admin.show_postlist"))


@admin.route("/admin/users/")
@login_required
@admin_required
def show_userlist() -> str:
    users = User.get_all()
    return render_template(template_name_or_list="users.html", users=users)


@admin.route("/admin/user/<string:user_id>/", methods=["GET", "POST"])
@login_required
@admin_required
def update_user(user_id: str) -> Response | str:
    user = User.get_by_user_id(user_id)

    if not user:
        abort(404)

    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        user.is_admin = form.is_admin.data
        user.save()
        return redirect(url_for("admin.show_userlist"))

    return render_template(template_name_or_list="show_user.html", form=form, user=user)


@admin.route("/admin/delete/<string:user_id>/", methods=["GET", "POST"])
@login_required
@admin_required
def delete_user(user_id: str) -> Response:
    user = User.get_by_user_id(user_id)

    if not user:
        abort(404)

    user.delete()
    return redirect(url_for("admin.show_userlist"))
