import base64
import binascii
from datetime import datetime

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


@public.route("/p/archive/<string:url_date>")
def archive(url_date: str) -> Response | str:
    try:
        date_str = base64.urlsafe_b64decode(url_date).decode()
        date = datetime.strptime(date_str, "%d-%m-%YT%H:%M:%S")
        posts = Post.get_by_date(date)

    except (binascii.Error, UnicodeDecodeError) as bad_decode:
        abort(400)

    except ValueError as bad_date:
        abort(400)

    return render_template(template_name_or_list="archive.html", selected_date=date, posts=posts)


@public.route("/profile/<string:user_id>")
def profile(user_id: str) -> Response | str:
    user = User.get_by_user_id(user_id)

    if user is None:
        abort(404)
    if not current_user.is_anonymous:
        if user.user_id == current_user.user_id:
            return redirect(url_for(endpoint='profile.index'))

    return render_template(template_name_or_list="public_profile.html", user=user)
