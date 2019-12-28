#Blueprint for user login and logout

from tv import login_manager, db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Blueprint, flash, redirect, render_template, request
from data import User
from forms import LoginForm, ChangePasswordForm

login_page = Blueprint("login", __name__)

# Login page
@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect("/admin")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect("/login")

        login_user(user, remember=False)
        return redirect('/admin')

    return render_template('login.html', title='Sign In', form=form)

# Logs out the current user
@login_page.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out")
    return redirect("/login")

# Change password for current user
@login_page.route("/admin/change_password", methods=['GET', 'POST'])
@login_required
def modify():
  user = User.query.filter_by(id=current_user.id).first()
  if user == None:
    flash("Invalid user id")
    return redirect("/admin")

  form = ChangePasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash('Your password has been changed, please log in again')
    return redirect("/logout")

  return render_template('change_password.html', form=form, user=user)
