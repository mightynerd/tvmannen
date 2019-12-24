from flask import Flask, render_template, flash, redirect, request, json

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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


@app.route("/pr")
def pr():
    priority = PR.query.filter_by(priority=1).first() 
    if priority != None:
        return json.jsonify(
            ["/static/pr/" + priority.file_name]
        )

    return json.jsonify(
        [("/static/pr/" + user.file_name) 
        for user in PR.query.all()]
        )