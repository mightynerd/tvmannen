#Blueprint for user login and logout

from tv import login_manager
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Blueprint, flash, redirect, render_template, request
from data import User
from forms import LoginForm

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
