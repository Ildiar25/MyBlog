from urllib.parse import urlparse

from flask import abort, Flask, redirect, render_template, request, Response, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, PostForm, SignupForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///instance/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)


from models import User, Post


@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)


@app.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)

    return render_template("post_view.html", post=post)


@app.route("/admin/post/", methods=["GET", "POST"])
@app.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_form(post_id: int | None = None) -> Response | str:
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        return redirect(url_for("index"))

    return render_template("admin/post_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()
    email_error = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)

        if user is not None:
            email_error = f"El email {email} ya está siendo utilizado por otro usuario"
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            login_user(user)

            next_page = request.args.get("next", None)

            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("index")

            return redirect(next_page)

    return render_template("signup_form.html", form=form, error=email_error)


@app.route("/login/", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

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
    return User.get_by_id(int(user_id))
