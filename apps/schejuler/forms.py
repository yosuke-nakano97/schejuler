from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.validators import URL

class RegisterForm(FlaskForm):
    username = StringField(
        "channel_url",
        validators=[
            URL(message="incorrect url")
        ],
    )
    submit = SubmitField("upload")