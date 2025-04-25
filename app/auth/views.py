from urllib.parse import urlparse

from flask import redirect, render_template, request, Response, url_for
from flask_login import current_user, login_user, logout_user

from app import login_manager
from . import auth
from .forms import LoginForm, SignupForm
from .models import User


@auth.route("/login/", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = LoginForm()
    email_error = None

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

        if user is None:
            email_error = f"El usuario '{form.email.data}' no existe."

        else:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                user.update_last_login()
                user.save()

                next_page = request.args.get("next")

                if not next_page or urlparse(next_page).netloc != "":
                    next_page = url_for("public.index")

                return redirect(next_page)

    return render_template(template_name_or_list="login.html", form=form, error=email_error)


@auth.route("/logout/")
def logout() -> Response:
    logout_user()
    return redirect(url_for("public.index"))


@auth.route("/signup/", methods=["GET", "POST"])
def signup() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = SignupForm()
    email_error = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)

        if user is not None:
            email_error = f"El email {email} ya está siendo utilizado por otro usuario."

        else:
            user = User(fullname=name, email=email)
            user.set_password(password)
            user.save()

            login_user(user)

            next_page = request.args.get("next", None)

            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("public.index")

            return redirect(next_page)

    return render_template(template_name_or_list="signup.html", form=form, error=email_error)


@login_manager.user_loader
def user_loader(user_id: str) -> User | None:
    return User.get_by_user_id(user_id)
