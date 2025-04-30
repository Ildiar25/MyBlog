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
    return render_template(template_name_or_list="index.html", post_pagination=post_pagination)


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
