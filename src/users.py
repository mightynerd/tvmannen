# Blueprint for user management in /admin/users and /admin/users/delete

from tv import login_manager, db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Blueprint, flash, redirect, render_template, request
from data import User
from forms import RegistrationForm, ModifyUserForm

users_page = Blueprint("users", __name__)

# Page for listing, creating and deleting users
@users_page.route('/admin/users', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != "admin":
        flash("You don't have permissions to manage users")
        return redirect("/admin")

    # Logged in as admin
    users = User.query.all()

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been created')
        return redirect("/admin/users")
    return render_template('users.html', form=form, users=users)

# Deletes an user on request for admin accounts
# Takes user_id "id" as argument
@users_page.route("/admin/users/delete")
@login_required
def delete_user():
    if current_user.role != "admin":
        flash("You don't have permissions to manage users")
        redirect("/admin")

    id = request.args.get("id")
    if id == None:
        flash("Invalid arguments")
        return redirect("/admin")

    user = User.query.filter_by(id=id).first()
    if user == None:
        flash("Id does not exist")
        return redirect("/admin/users")

    db.session.delete(user)
    db.session.commit()
    return redirect("/admin/users")

@users_page.route("/admin/users/modify", methods=['GET', 'POST'])
@login_required
def modify():
  if current_user.role != "admin":
        flash("You don't have permissions to manage users")
        redirect("/admin")

  id = request.args.get("id")
  if id == None:
      flash("Invalid arguments")
      return redirect("/admin/users")
  
  user = User.query.filter_by(id=id).first()
  if user == None:
    flash("Invalid user id")
    return redirect("/admin/users")

  form = ModifyUserForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    user.role = form.role.data
    print("Role set to:", form.role.data)
    db.session.commit()
    flash('The user has been sucessfully modified')
    return redirect("/admin/users")
  else: form.role.data = user.role
  return render_template('modify_user.html', form=form, user=user)

