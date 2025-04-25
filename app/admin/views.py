from flask import redirect, render_template, Response, url_for
from flask_login import current_user, login_required

from app.auth.decorators import admin_required
from app.public.models import Post

from . import admin
from .forms import PostForm


@admin.route("/admin/post/", methods=["GET", "POST"])
@admin.route("/admin/post/<string:slug>/", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(slug: str | None) -> Response | str:
    form = PostForm()

    if not slug:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_post = Post(title=title, content=content, user_id=current_user.user_id)
            new_post.save()

            return redirect(url_for("public.index"))
    else:
        post = Post.get_by_slug(slug)
        print(post)

    return render_template(template_name_or_list="create_post.html", form=form)
