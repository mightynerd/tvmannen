import os
curdir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "verysecretXd"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(curdir, 'db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(curdir, "static", "pr")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
