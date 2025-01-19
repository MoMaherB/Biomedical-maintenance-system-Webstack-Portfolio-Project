from maintenance_system import db , login_manager
from maintenance_system.Main import default_time
from flask_login import  UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

db.Table('user_task', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('task_id', db.Integer, db.ForeignKey('task.id')))

db.Table('user_hospital', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	rank = db.Column(db.String(120), default="Junior")
	profile_pic = db.Column(db.String(120), default="default.jpg")
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	machines = db.relationship('Machine', backref='user', lazy=True)
	hospitals = db.relationship('Hospital', secondary='user_hospital', backref='users', lazy='dynamic')
	
	def __repr__(self):
		return f'<User: {self.username}> - Email: {self.email}, Rank: {self.rank}' 
	
class Department(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	members = db.relationship('User', backref='department', lazy=True)
	devices = db.relationship('Device', backref='department', lazy=True)
	
	def __repr__(self):
		for user in self.members:
			print(user.username)
		return f'<Department: {self.name}>'
	
class Device(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	models = db.relationship('Model', backref='device', lazy=True)
	
	def __repr__(self):
		return f'<Device: {self.name}>'

class Model(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	manufacturer = db.Column(db.String(80))
	picture = db.Column(db.String(20), default='device_model.jpg')
	device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
	machines = db.relationship('Machine', backref='model', lazy=True)	
	def __repr__(self):
		return f'<Model: {self.name}>'
	
# db.Table('machine_hospital',
# 		db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')),
# 		db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')))

db.Table('machine_task',
		db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')),
		db.Column('task_id', db.Integer, db.ForeignKey('task.id')))

class Machine(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	serial_number = db.Column(db.String(80), unique=True)
	installation_date = db.Column(db.DateTime)
	contract_type = db.Column(db.Integer, default=int(0)) # 0: warranty, 1: maintenance, 2: none
	contract_name = db.Column(db.String(80))
	contract_start_date = db.Column(db.DateTime)
	contract_end_date = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
	hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
	tasks = db.relationship('Task', secondary='machine_task', backref='machines', lazy='dynamic')
	def __repr__(self):
		return f'<Machine: {self.serial_number}>'
	
class Hospital(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	governorate = db.Column(db.String(80))
	tasks = db.relationship('Task', backref='hospital', lazy=True)
	machines = db.relationship('Machine', backref='hospital', lazy=True)



class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task_type = db.Column(db.String(80))
	status = db.Column(db.Integer, default=int(0)) # 0: not completed, 1: in progress, 2: done
	open_date = db.Column(db.DateTime, nullable=False, default=default_time)
	close_date = db.Column(db.DateTime)
	description = db.Column(db.String(200))
	result = db.Column(db.String(200))
	hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
	users = db.relationship('User', secondary='user_task', backref='tasks', lazy='dynamic')



	
	def __repr__(self):
		return f'<Hospital: {self.name}>'
