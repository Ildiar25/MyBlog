from flask import abort, current_app, render_template, request, Response

from app.auth.models import User

from . import public
from .models import Post


@public.route("/")
def index() -> Response | str:
    page = int(request.args.get("page", 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page=page, per_page=per_page)
    return render_template(template_name_or_list="index.html", post_pagination=post_pagination)


@public.route("/p/<string:slug>/")
def show_posts(slug: str):
    post = Post.get_by_slug(slug)
    user = User.get_by_user_id(post.get_user_id)

    if post is None:
        abort(404)

    return render_template(template_name_or_list="show_post.html", post=post, user=user)
