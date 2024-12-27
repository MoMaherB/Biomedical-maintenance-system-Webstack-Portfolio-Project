from flask import render_template, redirect, url_for, flash, request
from maintenance_system import app, db
from maintenance_system.models import User , Department, Device, Model, Machine, Hospital
from maintenance_system.forms import UserForm, DepartmentForm, DeviceForm, ModelForm, MachineForm, HospitalForm



@app.route("/")
def home():
	return render_template("home.html")


#======================================User Routes========================================


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

#====================================Department Routes======================================


@app.route('/departments/', methods=['GET', 'POST'])
def departments():
	form = DepartmentForm()
	departments = Department.query.all()
	return render_template('departments.html', departments=departments, form=form)

@app.route('/departments/<int:id>/')
def department(id):
	department = Department.query.get_or_404(id)
	return render_template('department.html',department=department )

@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
	form = DepartmentForm()
	if request.method == 'GET':
		return redirect(url_for('departments'))
	elif form.validate_on_submit():
		new_department = Department(name=form.name.data)
		db.session.add(new_department)
		db.session.commit()
		flash(f'Department {form.name.data} has been created successfully!', 'success')
		return redirect(url_for('departments'))
	
	departments = Department.query.all()
	flash('Department name already exists. Please choose another one.', 'danger')
	return render_template('departments.html', form=form, departments=departments)

@app.route('/delete_department/<int:id>', methods=['POST'])
def delete_department(id):
	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash(f'Department {department.name} has been deleted successfully!', 'success')
	return redirect(url_for('departments'))

@app.route('/update_department/<int:id>', methods=['GET', 'POST'])
def update_department(id):
	department = Department.query.get_or_404(id)
	form = DepartmentForm()
	if request.method == 'GET':
		return redirect(url_for('departments'))
	elif form.validate_on_submit():
		department.name = form.name.data
		db.session.commit()
		flash('Department has been updated successfully!', 'success')
		return redirect(url_for('departments'))
	else:
		if form.name.data == department.name:
			flash('No changes detected. Nothing to update.', 'info')
		else:
			flash('Department name already exists. Please choose another one.', 'danger')
		return redirect(url_for('departments'))

#====================================Devices Routes======================================

#show all devices of a department and add new device
@app.route('/departments/<int:department_id>/devices/', methods=['GET'])
def devices(department_id):
	department = Department.query.get_or_404(department_id)
	form = DeviceForm()
	devices = department.devices
	return render_template('devices.html', department=department, devices=devices, form=form)

@app.route('/dpeartments/<int:department_id>/add_device', methods=['GET', 'POST'])
def add_device(department_id):
	form = DeviceForm()
	if request.method == 'GET':
		return redirect(url_for('devices', department_id=department_id))
	elif form.validate_on_submit():
		device = Device(name=form.name.data, department_id=department_id)
		db.session.add(device)
		db.session.commit()
		flash(f'Device {form.name.data} has been created successfully!', 'success')
		return redirect(url_for('devices', department_id=department_id))
	else:
		department = Department.query.get_or_404(department_id)
		devices = department.devices
		flash('Device name already exists. Please choose another one.', 'danger')
		return render_template('devices.html', department=department, devices=devices, form=form)

@app.route('/devices/<int:device_id>')
def device(device_id):
	device = Device.query.get_or_404(device_id)
	return render_template('device.html', device=device)

@app.route('/delete_device/<int:device_id>', methods=['POST'])
def delete_device(device_id):
	device = Device.query.get_or_404(device_id)
	db.session.delete(device)
	db.session.commit()
	flash(f'Device {device.name} has been deleted successfully!', 'success')
	return redirect(url_for('devices', department_id=device.department_id))

@app.route('/update_device/<int:device_id>', methods=['GET', 'POST'])
def update_device(device_id):
	device = Device.query.get_or_404(device_id)
	form = DeviceForm()
	if request.method == 'GET':
		return redirect(url_for('devices', department_id=device.department_id))
	elif form.validate_on_submit():
		device.name = form.name.data
		db.session.commit()
		flash('Device has been updated successfully!', 'success')
		return redirect(url_for('devices', department_id=device.department_id))
	else:
		if form.name.data == device.name:
			flash('No changes detected. Nothing to update.', 'info')
		else:
			flash('Device name already exists. Please choose another one.', 'danger')
		
		return redirect(url_for('devices', department_id=device.department_id))

#====================================Model Routes======================================

@app.route('/devices/<int:device_id>/models/', methods=['GET'])
def models(device_id):
	form = ModelForm()
	device = Device.query.get_or_404(device_id)
	models = device.models
	return render_template('models.html', device=device, models=models, form=form)

@app.route('/devices/<int:device_id>/add_model', methods=['GET', 'POST'])
def add_model(device_id):
	device = Device.query.get_or_404(device_id)
	models = device.models
	form = ModelForm()
	if request.method == 'GET':
		return redirect(url_for('models', device_id=device_id))
	elif form.validate_on_submit():
		New_model = Model(name=form.name.data, manufacturer=form.manufacturer.data, device_id=device_id)
		db.session.add(New_model)
		db.session.commit()
		flash(f'Model {form.name.data} has been created successfully!', 'success')
		return redirect(url_for('models', device_id=device_id))
	else:
		flash('Device name already exists. Please choose another one.', 'danger')
		return render_template('models.html', device=device, models=models, form=form)
	
@app.route('/delete_model/<int:model_id>', methods=['POST'])
def delete_model(model_id):
	model = Model.query.get_or_404(model_id)
	device = model.device
	db.session.delete(model)
	db.session.commit()
	flash(f'Model {model.name} has been deleted successfully!', 'success')
	return redirect(url_for('models', device_id=device.id))


@app.route('/update_model/<int:model_id>', methods=['GET', 'POST'])
def update_model(model_id):
	model = Model.query.get_or_404(model_id)
	form = ModelForm()
	if request.method == 'GET':
		return redirect(url_for('models', device_id=model.device_id))
	elif form.validate_on_submit():
		model.name = form.name.data
		model.manufacturer = form.manufacturer.data
		db.session.commit()
		flash(f'Model { model.name }has been updated successfully!', 'success')
		return redirect(url_for('models', device_id=model.device_id))
	else:
		if form.name.data == model.name:
			flash('No changes detected. Nothing to update.', 'info')
		else:
			flash('Model name already exists. Please choose another one.', 'danger')
		
		return redirect(url_for('models', device_id=model.device_id))
	
#======================================Machine Routes========================================

@app.route('/models/<int:model_id>/machines/', methods=['GET'])
def machines(model_id):
	model = Model.query.get_or_404(model_id)
	machines = model.machines
	return render_template('machines.html',
				model=model, machines=machines)

@app.route('/models/<int:model_id>/add_machine', methods=['GET', 'POST'])
def add_machine(model_id):
	model = Model.query.get_or_404(model_id)
	form = MachineForm()
	name = 'Add'
	if form.validate_on_submit():
		machine = Machine(serial_number=form.serial_number.data,
					model_id=model_id,
					installation_date=form.installation_date.data,
					contract_type=form.contract_type.data,
					contract_name=form.contract_name.data,
					contract_start_date=form.contract_start_date.data,
					contract_end_date=form.contract_end_date.data)
		db.session.add(machine)
		db.session.commit()
		flash(f'Machine  number {form.serial_number.data} for {model.name} {model.device.name} has been created successfully!', 'success')
		return redirect(url_for('machines', model_id=model_id))

	return render_template('add_machine.html', model=model, form=form, name=name)

@app.route('/machines/<int:machine_id>')
def machine(machine_id):
	machine = Machine.query.get_or_404(machine_id)
	return render_template('machine.html', machine=machine)

@app.route('/delete_machine/<int:machine_id>', methods=['POST'])
def delete_machine(machine_id):
	machine = Machine.query.get_or_404(machine_id)
	model = machine.model
	db.session.delete(machine)
	db.session.commit()
	flash(f'Machine {machine.serial_number} has been deleted successfully!', 'success')
	return redirect(url_for('machines', model_id=model.id))
	
@app.route('/update_machine/<int:machine_id>', methods=['GET', 'POST'])
def update_machine(machine_id):
	machine = Machine.query.get_or_404(machine_id)
	form = MachineForm()
	name = 'Update'
	if form.validate_on_submit() or (request.method == 'POST' and form.serial_number.data == machine.serial_number):
		machine.serial_number = form.serial_number.data
		machine.installation_date = form.installation_date.data
		machine.contract_type = form.contract_type.data
		machine.contract_name = form.contract_name.data
		machine.contract_start_date = form.contract_start_date.data
		machine.contract_end_date = form.contract_end_date.data
		db.session.commit()
		flash('Machine has been updated successfully!', 'success')
		return redirect(url_for('machines', model_id=machine.model_id))
	form.serial_number.data = machine.serial_number
	form.installation_date.data = machine.installation_date
	form.contract_type.data = machine.contract_type
	form.contract_name.data = machine.contract_name
	form.contract_start_date.data = machine.contract_start_date
	form.contract_end_date.data = machine.contract_end_date
	form.submit.label.text = 'Update'
	return render_template('add_machine.html', form=form, machine=machine, name=name)
	

	#======================================Hospital Routes========================================

@app.route('/hospitals')
def hospitals():
	hospitals = Hospital.query.all()
	return render_template('hospitals.html', hospitals=hospitals)

@app.route('/hospitals/<int:id>')
def hospital(id):
	hospital = Hospital.query.get_or_404(id)
	return render_template('hospital.html', hospital=hospital)

@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
	form_name = 'Add'
	form = HospitalForm()
	if form.validate_on_submit():
		hospital = Hospital(name=form.name.data, governorate=form.governorate.data.capitalize().strip())
		db.session.add(hospital)
		db.session.commit()
		flash('Hospital has been created successfully!', 'success')
		return redirect(url_for('hospitals'))
	return render_template('add_hospital.html', form=form, form_name=form_name)

@app.route('/delete_hospital/<int:id>', methods=['POST'])
def delete_hospital(id):
	hospital = Hospital.query.get_or_404(id)
	db.session.delete(hospital)
	db.session.commit()
	flash(f'Hospital {hospital.name} has been deleted successfully!', 'success')
	return redirect(url_for('hospitals'))

@app.route('/update_hospital/<int:id>', methods=['GET', 'POST'])
def update_hospital(id):
	hospital = Hospital.query.get_or_404(id)
	form_name = 'Update'
	form = HospitalForm()
	if form.validate_on_submit() or (request.method == 'POST' and form.name.data == hospital.name):
		hospital.name = form.name.data
		hospital.governorate = form.governorate.data.capitalize().strip()
		db.session.commit()
		flash('Hospital has been updated successfully!', 'success')
		return redirect(url_for('hospitals'))
	form.name.data = hospital.name
	form.governorate.data = hospital.governorate
	form.submit.label.text = 'Update'
	return render_template('add_hospital.html', form=form, form_name=form_name)



@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return f"Caught route: {path}", 404
