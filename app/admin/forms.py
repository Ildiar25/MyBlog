from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """"""

    # Form fields
    title = StringField(label="Título", validators=[DataRequired(), Length(max=128)])
    content = TextAreaField(label="Contenido")
    submit = SubmitField(label="Guardar")

    def __repr__(self) -> str:
        return (
            f"<class PostForm("
            f"title={repr(self.title.label)}, "
            f"content={repr(self.content.label)}, "
            f"submit={repr(self.submit.label)}, "
            f")>"
        )
