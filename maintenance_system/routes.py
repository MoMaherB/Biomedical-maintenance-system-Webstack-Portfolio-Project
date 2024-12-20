from flask import render_template, redirect, url_for, flash, request
from maintenance_system import app, db
from maintenance_system.models import User , Department
from maintenance_system.forms import UserForm, DepartmentForm, UpdateDepartmentForm



@app.route("/")
def home():
	return render_template("home.html")


#==================User Routes============================

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = UserForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('User has been created successfully!', 'success')
		return redirect(url_for('users'))
	return render_template('register.html', form=form)

@app.route('/users')
def users():
	users = User.query.all()
	return render_template('users.html', users=users)

@app.route('/users/<int:id>')
def user(id):
	user = User.query.get_or_404(id)
	return render_template('user.html', user=user)

#=================Department Routes==========================

@app.route('/departments/')
def departments():
	departments = Department.query.all()
	return render_template('departments.html', departments=departments)

@app.route('/departments/<int:id>')
def department(id):
	department = Department.query.get_or_404(id)

	return render_template('department.html',department=department )

@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
	departments = Department.query.all()
	form = DepartmentForm()
	if form.validate_on_submit():
		new_department = Department(name=form.name.data)
		db.session.add(new_department)
		db.session.commit()
		return redirect(url_for('departments'))
	
	return render_template('departments.html', form=form, departments=departments)

@app.route('/delete_department/<int:id>')
def delete_department(id):
	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	return redirect(url_for('departments'))

@app.route('/update_department/<int:id>', methods=['GET', 'POST'])
def update_department(id):
	departments = Department.query.all()
	department = Department.query.get_or_404(id)
	form = UpdateDepartmentForm()
	if form.validate_on_submit():
		department.name = form.name.data
		db.session.commit()
		return redirect(url_for('departments'))
	elif request.method == 'GET':
		form.name.data = department.name
	return render_template('departments.html', form=form, departments=departments)
