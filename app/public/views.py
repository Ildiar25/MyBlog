from flask import abort, render_template, Response
from . import public
from .models import Post


@public.route("/")
def index() -> Response | str:
    posts = Post.get_all()
    return render_template(template_name_or_list="index.html", posts=posts)


@public.route("/p/<string:slug>/")
def show_posts(slug: str):
    post = Post.get_by_slug(slug)

    if post is None:
        abort(404)

    return render_template(template_name_or_list="show_post.html", post=post)
