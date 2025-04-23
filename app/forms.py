from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    submit = SubmitField("Registrar")


class PostForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(max=128)])
    title_slug = StringField("Título Slug", validators=[DataRequired(), Length(max=128)])
    content = TextAreaField("Contenido")
    submit = SubmitField("Guardar")


class LoginForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Iniciar Sesión")
