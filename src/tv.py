from flask import Flask, render_template, flash, redirect, request
import os
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm
from werkzeug.utils import secure_filename

from config import Config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from data import User, PR, add_pr

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            org_filename = secure_filename(file.filename)
            # Generate random filename with correct extention
            filename = str(uuid.uuid4()) + "." + org_filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_pr(file_name=filename, desc="lel", start_date=datetime.now(), end_date=datetime.now(), user_id=current_user.id)
            return "done"

    if current_user.role == "admin":
        pr = PR.query.all()
    else:
        pr = PR.query.filter_by(user_id=current_user.id)
    return render_template("admin.html", user=current_user, pr_list = pr)

@app.route("/admin/users")
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("You don't have permissions to visit this page")
        return redirect("/login")

    return "Admin"

@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"


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

