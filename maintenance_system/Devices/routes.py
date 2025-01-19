from flask import render_template, request, redirect, url_for, flash, Blueprint
from maintenance_system import db
from maintenance_system.models import Department, Device
from .forms import DeviceForm

devicesbp = Blueprint('devicesbp', __name__)


@devicesbp.route('/departments/<int:department_id>/devices/', methods=['GET'])
def devices(department_id):
    """Get all devices in a department"""
    department = Department.query.get_or_404(department_id)
    form = DeviceForm()
    devices = department.devices
    return render_template('devices.html', department=department, devices=devices, form=form)


@devicesbp.route('/dpeartments/<int:department_id>/add_device', methods=['GET', 'POST'])
def add_device(department_id):
    """Add a new device to a department"""
    form = DeviceForm()
    if request.method == 'GET':
        return redirect(url_for('devices', department_id=department_id))
    elif form.validate_on_submit():
        device = Device(name=form.name.data, department_id=department_id)
        db.session.add(device)
        db.session.commit()
        flash(f'Device {form.name.data} has been created successfully!', 'success')
        return redirect(url_for('devicesbp.devices', department_id=department_id))
    else:
        department = Department.query.get_or_404(department_id)
        devices = department.devices
        flash('Device name already exists. Please choose another one.', 'danger')
        return render_template('devices.html', department=department, devices=devices, form=form)


@devicesbp.route('/devices/<int:device_id>')
def device(device_id):
    """Get a device by id"""
    device = Device.query.get_or_404(device_id)
    return render_template('device.html', device=device)


@devicesbp.route('/delete_device/<int:device_id>', methods=['POST'])
def delete_device(device_id):
    """Delete a device by id"""
    device = Device.query.get_or_404(device_id)
    for model in device.models:
        for machine in model.machines:
            db.session.delete(machine)
        db.session.delete(model)
    db.session.delete(device)
    db.session.commit()
    flash(f'Device {device.name} has been deleted successfully!', 'success')
    return redirect(url_for('devicesbp.devices', department_id=device.department_id))


@devicesbp.route('/update_device/<int:device_id>', methods=['GET', 'POST'])
def update_device(device_id):
    """Update a device by id"""
    device = Device.query.get_or_404(device_id)
    form = DeviceForm()
    if request.method == 'GET':
        return redirect(url_for('devicesbp.devices', department_id=device.department_id))
    elif form.validate_on_submit():
        device.name = form.name.data
        db.session.commit()
        flash('Device has been updated successfully!', 'success')
        return redirect(url_for('devicesbp.devices', department_id=device.department_id))
    else:
        if form.name.data == device.name:
            flash('No changes detected. Nothing to update.', 'info')
        else:
            flash('Device name already exists. Please choose another one.', 'danger')

        return redirect(url_for('devicesbp.devices', department_id=device.department_id))
