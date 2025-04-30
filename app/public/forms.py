from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    """"""

    # Form fields
    content = TextAreaField(label="Contenido", validators=[DataRequired()])
    submit = SubmitField(label="Comentar")

    def __repr__(self) -> str:
        return (
            f"<class CommentForm("
            f"content={repr(self.content.label)}, "
            f"submit={repr(self.submit.label)}, "
            f")>"
        )
