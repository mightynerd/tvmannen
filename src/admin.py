# Blueprint for admin page with PR management

from tv import login_manager, db, config, app
import os
import uuid
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Blueprint, flash, redirect, render_template, request
from data import User, PR, add_pr, fix_date
from forms import PRForm, ModifyPRForm
from werkzeug.utils import secure_filename

admin_page = Blueprint("admin", __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Admin page with PR list, upload and deletion
@admin_page.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    form = PRForm()
    if form.validate_on_submit():
        filename = form.file.data.filename
        if filename and allowed_file(filename):
            org_filename = secure_filename(filename)
            # Generate random filename with correct extention
            filename = str(uuid.uuid4()) + "." + \
                org_filename.rsplit('.', 1)[1].lower()
            form.file.data.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
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
    return render_template("admin.html", user=current_user, pr_list=pr, form=form)

# Deletes a PR on request if the current user has the right permissions
# Takes PR id "id" as argument
@admin_page.route("/admin/delete")
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

    try:
        os.remove(os.path.join(config.UPLOAD_FOLDER, pr.file_name))
    except: 
        flash("PR wasn't found on disk but the database entry has been removed")
        
    db.session.delete(pr)
    db.session.commit()
    flash("PR successfully deleted")
    return redirect("/admin")


@admin_page.route("/admin/modify_pr", methods=['GET', 'POST'])
@login_required
def modify():
  id = request.args.get("id")
  if id == None:
      flash("Invalid arguments")
      return redirect("/admin")

  pr = PR.query.filter_by(id=id).first()
  if pr == None:
    flash("Invalid PR id")
    return redirect("/admin")

  if current_user.role != "admin" and current_user.id != pr.user_id:
        flash("You don't have permissions to modify this PR")
        redirect("/admin")

  form = ModifyPRForm()
  if form.validate_on_submit():
    start, end = fix_date(form.start_date.data, form.end_date.data)
    pr.start_date = start
    pr.end_date = end
    db.session.commit()
    flash('The PR has been sucessfully modified')
    return redirect("/admin")
  else:
      form.start_date.data = pr.start_date
      form.end_date.data = pr.end_date
  return render_template('modify_pr.html', form=form, pr=pr)
