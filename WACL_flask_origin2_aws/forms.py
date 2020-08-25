from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    """아이디 입력 및 역학조사 시작 form """
    ID = StringField('ID', validators=[Required()])
    submit = SubmitField('Search start!')
