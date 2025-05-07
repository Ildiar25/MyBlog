from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    """"""

    # Form fields
    fullname = StringField(label="Nombre completo", validators=[DataRequired(), Length(max=64)])
    profile_pic = FileField(
        label="Foto de Perfil", validators=[FileAllowed(upload_set=["jpg", "png"], message="Sólo se permite JPG o PNG")]
    )
    about_me = TextAreaField(validators=[Length(max=512)])
    submit = SubmitField("Guardar")

    def __repr__(self) -> str:
        return (
            f"<class ProfileForm("
            f"fullname={repr(self.fullname.label)}, "
            f"profile_pic={repr(self.profile_pic.label)}, "
            f"about_me={repr(self.profile_pic.label)}, "
            f"submit={repr(self.submit.label)}, "
            f")>"
        )
