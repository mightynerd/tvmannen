from tv import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32))

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)


class PR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(128))
    file_name = db.Column(db.String(128))
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priority = db.Column(db.Integer, default=0)
    

def add_pr(file_name, desc, priority, start_date, end_date, user_id):
  # Shift datetimes to the day after at 5:00
  start = datetime(
            year=start_date.year, 
            month=start_date.month, 
            day=start_date.day + 1, 
            hour=5
          )

  end = datetime(
          year=end_date.year, 
          month=end_date.month, 
          day=end_date.day + 1, 
          hour=5
        )

  pr = PR(desc=desc, file_name=file_name, priority=priority,
          start_date=start, end_date=end, user_id=user_id)
  db.session.add(pr)
  db.session.commit()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_db():
  db.create_all()
  u = User(id=0, username="admin", role="admin")
  u.set_password("pass")
  db.session.add(u)
  u = User(id=1, username="pr", role="pr")
  u.set_password("pass")
  db.session.add(u)
  db.session.commit()
