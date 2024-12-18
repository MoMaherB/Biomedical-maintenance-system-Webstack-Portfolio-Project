from flask import render_template, redirect, url_for
from maintenance_system import app, db
from maintenance_system.models import User
from maintenance_system.forms import UserForm



@app.route("/")
def home():
	return render_template("home.html")


#==================User Routes============================

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = UserForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('users'))
	return render_template("register.html", form=form)