from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from tv import User
from datetime import datetime

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
  today = datetime.today()
  tomorrow = today.replace(day=today.day + 1)

  file = FileField("Image file", validators=[DataRequired()])
  desc = StringField("Description", validators=[DataRequired()])
  start_date = DateField("Start date (first day the PR will be shown):",
                         validators=[DataRequired()], default=today)
  end_date = DateField("End date (last day the PR will be shown):"
                       , validators=[DataRequired()], default=tomorrow)
  priority = BooleanField("Priority")
  submit = SubmitField('Upload PR')
