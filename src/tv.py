from flask import Flask, render_template, flash, redirect, request, json

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

from config import Config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from data import PR

from users import users_page
app.register_blueprint(users_page)

from admin import admin_page
app.register_blueprint(admin_page)

from login import login_page
app.register_blueprint(login_page)

@app.route('/')
@app.route('/index')
def index():
    return render_template("pr.html")

# Delete old PRs
def pr_cleanup():
    PR.query.filter(PR.end_date < datetime.now()).delete()
    db.session.commit()

@app.route("/pr")
def pr():
    pr_cleanup()

    # Check if priority PR exists
    priority = PR.query.filter(PR.priority==1, PR.start_date < datetime.now()).first() 
    if priority != None:
        return json.jsonify(
            ["/static/pr/" + priority.file_name]
        )

    # Return all active PRs
    return json.jsonify(
        [("/static/pr/" + user.file_name) 
            for user in PR.query.filter(PR.start_date < datetime.now()).all()]
        )