from flask import render_template, request, redirect, url_for, flash, Blueprint
from maintenance_system import db
from maintenance_system.models import Device, Model
from .forms import ModelForm

modelsbp = Blueprint('modelsbp', __name__)


@modelsbp.route('/devices/<int:device_id>/models/', methods=['GET'])
def models(device_id):
    """Show all models for a specific device"""
    form = ModelForm()
    device = Device.query.get_or_404(device_id)
    models = device.models
    return render_template('models.html', device=device, models=models, form=form)


@modelsbp.route('/devices/<int:device_id>/add_model', methods=['GET', 'POST'])
def add_model(device_id):
    """Add a new model for a specific device"""
    device = Device.query.get_or_404(device_id)
    models = device.models
    form = ModelForm()
    if request.method == 'GET':
        return redirect(url_for('modelsbp.models', device_id=device_id))
    elif form.validate_on_submit():
        New_model = Model(name=form.name.data, manufacturer=form.manufacturer.data, device_id=device_id)
        db.session.add(New_model)
        db.session.commit()
        flash(f'Model {form.name.data} has been created successfully!', 'success')
        return redirect(url_for('modelsbp.models', device_id=device_id))
    else:
        flash('Device name already exists. Please choose another one.', 'danger')
        return render_template('models.html', device=device, models=models, form=form)


@modelsbp.route('/delete_model/<int:model_id>', methods=['POST'])
def delete_model(model_id):
    """Delete a specific model"""
    model = Model.query.get_or_404(model_id)
    device = model.device
    for machine in model.machines:
        db.session.delete(machine)
    db.session.delete(model)
    db.session.commit()
    flash(f'Model {model.name} has been deleted successfully!', 'success')
    return redirect(url_for('modelsbp.models', device_id=device.id))


@modelsbp.route('/update_model/<int:model_id>', methods=['GET', 'POST'])
def update_model(model_id):
    """Update a specific model"""
    model = Model.query.get_or_404(model_id)
    form = ModelForm()
    if request.method == 'GET':
        return redirect(url_for('models', device_id=model.device_id))
    elif form.validate_on_submit():
        model.name = form.name.data
        model.manufacturer = form.manufacturer.data
        db.session.commit()
        flash(f'Model { model.name }has been updated successfully!', 'success')
        return redirect(url_for('modelsbp.models', device_id=model.device_id))
    else:
        if form.name.data == model.name:
            flash('No changes detected. Nothing to update.', 'info')
        else:
            flash('Model name already exists. Please choose another one.', 'danger')

        return redirect(url_for('modelsbp.models', device_id=model.device_id))
