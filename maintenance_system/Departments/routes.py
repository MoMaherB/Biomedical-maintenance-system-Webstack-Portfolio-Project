from flask import render_template, request, redirect, url_for, flash, Blueprint
from maintenance_system import db
from maintenance_system.models import Department
from .forms import DepartmentForm


departmentsbp = Blueprint('departmentsbp', __name__)


@departmentsbp.route('/departments/', methods=['GET', 'POST'])
def departments():
    """Get all departments"""
    form = DepartmentForm()
    departments = Department.query.all()
    return render_template('departments.html', departments=departments, form=form)


@departmentsbp.route('/departments/<int:id>/')
def department(id):
    """Get a department by id"""
    department = Department.query.get_or_404(id)
    return render_template('department.html', department=department)


@departmentsbp.route('/add_department', methods=['GET', 'POST'])
def add_department():
    """Add a new department"""
    form = DepartmentForm()
    if request.method == 'GET':
        return redirect(url_for('departments'))
    elif form.validate_on_submit():
        new_department = Department(name=form.name.data)
        db.session.add(new_department)
        db.session.commit()
        flash(f'Department {form.name.data} has been created successfully!', 'success')
        return redirect(url_for('departmentsbp.departments'))

    departments = Department.query.all()
    flash('Department name already exists. Please choose another one.', 'danger')
    return render_template('departments.html', form=form, departments=departments)


@departmentsbp.route('/delete_department/<int:id>', methods=['POST'])
def delete_department(id):
    """Delete a department by id"""
    department = Department.query.get_or_404(id)
    for device in department.devices:
        for model in device.models:
            for machine in model.machines:
                db.session.delete(machine)
            db.session.delete(model)
        db.session.delete(device)
    db.session.delete(department)
    db.session.commit()
    flash(f'Department {department.name} has been deleted successfully!', 'success')
    return redirect(url_for('departmentsbp.departments'))


@departmentsbp.route('/update_department/<int:id>', methods=['GET', 'POST'])
def update_department(id):
    """Update a department by id"""
    department = Department.query.get_or_404(id)
    form = DepartmentForm()
    if request.method == 'GET':
        return redirect(url_for('departments'))
    elif form.validate_on_submit():
        department.name = form.name.data
        db.session.commit()
        flash('Department has been updated successfully!', 'success')
        return redirect(url_for('departmentsbp.departments'))
    else:
        if form.name.data == department.name:
            flash('No changes detected. Nothing to update.', 'info')
        else:
            flash('Department name already exists. Please choose another one.', 'danger')
        return redirect(url_for('departmentsbp.departments'))
