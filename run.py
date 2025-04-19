from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", num_posts=len(posts))


@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/", methods=["GET", "POST"])
@app.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
def post_form(post_id: int | None = None) -> str:
    return render_template("admin/post_form.html", post_id=post_id)


posts = []
