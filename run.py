from urllib.parse import urlparse

from flask import Flask, redirect, render_template, request, Response, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required

from forms import LoginForm, PostForm, SignupForm
from models import User, users, get_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.route("/")
def index():
    # page = request.args.get("page", 1)
    # posts = request.args.get("list", 20)
    return render_template("index.html", posts=total_posts)


@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/", methods=["GET", "POST"])
@app.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_form(post_id: int | None = None) -> Response | str:
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data

        post = {"title": title, "title_slug": title_slug, "content": content}
        total_posts.append(post)

        return redirect(url_for("index"))

    return render_template("admin/post_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(len(users) + 1, name, email, password)
        users.append(user)

        login_user(user)

        next_page = request.args.get("next", None)

        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template("signup_form.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = get_user(form.email.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")

            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("index")

            return redirect(next_page)

    return render_template("login_form.html", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def user_loader(user_id: str) -> User | None:
    for user in users:
        if user.user_id == int(user_id):
            return user

    return None


total_posts = []
