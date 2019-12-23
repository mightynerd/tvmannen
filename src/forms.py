from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from tv import User

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    roles = [('admin', "Admin"), ('pr', "PR")]

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField("Role",validators=[DataRequired()], choices=roles)
    submit = SubmitField('Create user')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken')

class PRForm(FlaskForm):
  file = FileField("Image file")
  desc = StringField("Description")
  start_date = DateField("Start date (first day the PR will be shown):", format='%Y-%m-%d')
  end_date = DateField("End date (last day the PR will be shown):", format='%Y-%m-%d')
  priority = BooleanField("Priority")
  submit = SubmitField('Upload PR')
