from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """"""

    # Form fields
    email = StringField(label="Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField(label="Contraseña", validators=[DataRequired()])
    remember_me = BooleanField(label="Recuérdame")
    submit = SubmitField(label="Iniciar Sesión")

    def __repr__(self) -> str:
        return (
            f"<class LoginForm("
            f"email={repr(self.email.label)}, "
            f"password={repr(self.password.label)}, "
            f"remember_me={repr(self.remember_me.label)}, "
            f"submit={repr(self.submit.label)}, "
            f")>"
        )


class SignupForm(FlaskForm):
    """"""

    # Form fields
    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=64)])
    password = PasswordField(label="Contraseña", validators=[DataRequired(), EqualTo("check_pw")])
    check_pw = PasswordField(label="Repite la contraseña", validators=[DataRequired(), EqualTo("password")])
    email = StringField(label="Correo electrónico", validators=[DataRequired(), Email()])
    submit = SubmitField("Registrar")

    def __repr__(self) -> str:
        return (
            f"<class SignupForm("
            f"name={repr(self.name.label)}, "
            f"password={repr(self.password.label)}, "
            f"check_password={repr(self.check_pw.label)}, "
            f"email={repr(self.email.label)}, "
            f"submit={repr(self.submit.label)}, "
            f")>"
        )
