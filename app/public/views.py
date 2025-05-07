from flask import abort, current_app, redirect, render_template, request, Response, url_for
from flask_login import current_user

from app.auth.models import User

from . import public
from .forms import CommentForm
from .models import Comment, Post


@public.route("/")
def index() -> Response | str:
    page = int(request.args.get("page", 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page=page, per_page=per_page)
    owner = User.get_by_email(current_app.config["WEB_OWNER"])
    return render_template(template_name_or_list="index.html", post_pagination=post_pagination, owner=owner)


@public.route("/p/<string:slug>/", methods=["GET", "POST"])
def show_posts(slug: str):
    post = Post.get_by_slug(slug)

    if post is None:
        abort(404)

    form = CommentForm()

    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.user_id, post_id=post.post_id)
        comment.save()

        return redirect(url_for(endpoint='public.show_posts', slug=post.slug_title))

    return render_template(template_name_or_list="show_post.html", post=post, form=form)


@public.route("/p/archive/<string:date>")
def archive(date: str) -> Response | str:
    print(date)
    print(type(date))
    posts = Post.get_by_date(date)

    return render_template(template_name_or_list="archive.html", posts=posts)


@public.route("/profile/<string:user_email>")
def profile(user_email: str) -> Response | str:
    user = User.get_by_email(user_email)
    return render_template(template_name_or_list="archive.html")
