from flask import render_template, url_for, flash, redirect, request, Blueprint
from maintenance_system import db
from maintenance_system.models import Department, Task, Machine, Model, Device, User, Hospital
from .forms import TaskForm
from maintenance_system.Main.default_time import default_time


taskpb = Blueprint('taskpb', __name__)

@taskpb.route('/departments/<int:department_id>/in_progress_tasks/', methods=['GET', 'POST'])
def in_progress_tasks(department_id):
    department = Department.query.get_or_404(department_id)
    
    tasks = Task.query.join(Task.machines).join(Machine.model).join(Model.device).filter(Device.department_id == department_id).all()
    tasks = [task for task in tasks if task.status == 0]
    return render_template('in_progress_tasks.html', department=department, tasks=tasks)

@taskpb.route('/departments/<int:department_id>/completed_tasks/', methods=['GET'])
def completed_tasks(department_id):
    department = Department.query.get_or_404(department_id)
    
    tasks = Task.query.join(Task.machines).join(Machine.model).join(Model.device).filter(Device.department_id == department_id).all()
    tasks = [task for task in tasks if task.status == 1]
    return render_template('completed_tasks.html', department=department, tasks=tasks)

@taskpb.route('/departments/<int:department_id>/add_task', methods=['GET', 'POST'])
def add_task(department_id):
    department = Department.query.get_or_404(department_id)
    form = TaskForm()

    # Populate initial choices
    form.user.choices = [(user.id, user.username) for user in department.members]
    form.governorate.choices += [
    (hospital.governorate, hospital.governorate) 
    for hospital in db.session.query(Hospital.governorate).group_by(Hospital.governorate).all()]

    form.device.choices += [(device.id, device.name) for device in department.devices]
    form.machine.choices = []

    
    # Handle governorate selection
    if form.governorate.data:
        hospitals = Hospital.query.filter_by(governorate=form.governorate.data).all()
        form.hospital.choices += [(hospital.id, hospital.name) for hospital in hospitals]

    # Handle device selection
    if form.device.data:
        device = Device.query.get_or_404(form.device.data)
        form.model.choices += [(model.id, model.name) for model in device.models]

    # Handle model selection
    if form.model.data:
        model = Model.query.get_or_404(form.model.data)
        try:
            hospital_id = int(request.form.get('hospital', 0))
        except ValueError:
            hospital_id = 0
        form.machine.choices += [
            (machine.id, machine.serial_number)
            for machine in model.machines
            if machine.hospital_id == hospital_id
        ]
   
    if form.validate_on_submit():
        # Handle final task submission
        print(form.data)
        machines = [Machine.query.get_or_404(int(machine_id)) for machine_id in form.machine.data]
        users = [User.query.get_or_404(int(user_id)) for user_id in form.user.data]
        print(users)
        print(machines)
        task = Task(
          task_type=form.task_type.data,
          description=form.description.data,
          hospital_id=int(form.hospital.data),
          machines=machines,
          users=users         
        )
        db.session.add(task)
        db.session.commit()
        flash('Task has been created successfully!', 'success')
        return redirect(url_for('taskpb.in_progress_tasks', department_id=department_id))
    print(form.data)
    return render_template('add_task.html', form=form, department=department)

@taskpb.route('/add_task_result/<int:task_id>', methods=['GET', 'POST'])
def add_task_result(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 1
    task.result = request.form.get('result')
    task.close_date = default_time()
    db.session.commit()
    flash('Task finished successfully!', 'success')
    return redirect(url_for('taskpb.completed_tasks', department_id=task.machines[0].model.device.department_id))

@taskpb.route('/delete_task/<int:task_id>', methods=['Get', 'POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    machine = task.machines[0]
    print(machine)
    db.session.delete(task)
    db.session.commit()
    flash(f'Task has been deleted successfully!', 'success')
    return redirect(url_for('taskpb.completed_tasks', department_id=machine.model.device.department_id))
