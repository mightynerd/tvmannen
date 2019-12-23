from flask import Flask, render_template, flash, redirect, request
import os
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from config import Config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from data import User, PR, add_pr
from forms import LoginForm, RegistrationForm, PRForm

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/admin/delete")
@login_required
def delete():
    id = request.args.get("id")
    if id == None:
        flash("Invalid arguments")
        return redirect("/admin")

    pr = PR.query.filter_by(id=id).first()
    if pr == None:
        flash("Id does not exist")
        return redirect("/admin")
    
    if current_user.role != "admin" and current_user.id != pr.user_id:
        flash("You don't have permissions to delete this pr")
        return redirect("/admin")

    os.remove(os.path.join(config.UPLOAD_FOLDER, pr.file_name))
    db.session.delete(pr)
    db.session.commit()
    flash("PR successfully deleted")
    return redirect("/admin")

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    #if request.method == 'POST':
    #    # check if the post request has the file part
    #    if 'file' not in request.files:
    #        flash('No file part')
    #        return redirect(request.url)
    #    file = request.files['file']
    #    # if user does not select file, browser also
    #    # submit an empty part without filename
    #    if file.filename == '':
    #        flash('No selected file')
    #        return redirect(request.url)
    #    if file and allowed_file(file.filename):
    #        org_filename = secure_filename(file.filename)
    #        # Generate random filename with correct extention
    #        filename = str(uuid.uuid4()) + "." + org_filename.rsplit('.', 1)[1].lower()
    #        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #        add_pr(file_name=filename, desc="lel", start_date=datetime.now(), end_date=datetime.now(), user_id=current_user.id)
    #        return redirect("/admin")
    form = PRForm()
    if form.validate_on_submit():
        filename = form.file.data.filename
        if filename and allowed_file(filename):
            org_filename = secure_filename(filename)
            # Generate random filename with correct extention
            filename = str(uuid.uuid4()) + "." + org_filename.rsplit('.', 1)[1].lower()
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_pr(file_name=filename, 
                   desc=form.desc.data, 
                   priority=form.priority.data,
                   start_date=form.start_date.data, 
                   end_date=form.end_date.data,
                   user_id=current_user.id)
            return redirect("/admin")

    if current_user.role == "admin":
        pr = PR.query.all()
    else:
        pr = PR.query.filter_by(user_id=current_user.id)
    return render_template("admin.html", user=current_user, pr_list = pr, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash ("Logged out")
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect("/admin")
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user == None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect("/login")

        login_user(user, remember=False)
        return redirect('/admin')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/admin/users', methods=['GET', 'POST'])
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

@app.route("/admin/users/delete")
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
    return redirect("/admin/users/")

