from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from data import User
from datetime import datetime

roles = [('admin', "Admin"), ('pr', "PR")]

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
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

  file = FileField(label="Image file:", validators=[DataRequired()])
  desc = StringField("Description:", validators=[DataRequired()]
                     , render_kw={"placeholder": "Hackkväll 24/12"})
  start_date = DateField("Start date:",
                         validators=[DataRequired()], default=today)
  end_date = DateField("End date:"
                       , validators=[DataRequired()], default=tomorrow)
  priority = BooleanField("Priority:")
  submit = SubmitField('Upload PR')

class ModifyUserForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  role = SelectField("Role", validators=[DataRequired()], choices=roles)
  submit = SubmitField('Save changes')
