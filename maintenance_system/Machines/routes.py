from flask import render_template, request, redirect, url_for, flash, Blueprint
from maintenance_system import db
from maintenance_system.models import Model, Machine, Hospital
from .forms import MachineForm

machinesbp = Blueprint('machinesbp', __name__)


@machinesbp.route('/models/<int:model_id>/machines/', methods=['GET'])
def machines(model_id):
    model = Model.query.get_or_404(model_id)
    machines = model.machines
    governorates = [
    hospital.governorate 
    for hospital in db.session.query(Hospital.governorate).group_by(Hospital.governorate).all()]
    hospitals = Hospital.query.all()
   
    if request.args.get('governorate'):
        machines = [machine for machine in machines if machine.hospital.governorate == request.args.get('governorate')]
        hospitals = [hospital for hospital in hospitals if hospital.governorate == request.args.get('governorate')]
    
    if request.args.get('hospital'):
        machines = [machine for machine in machines if machine.hospital_id == int(request.args.get('hospital'))]

    return render_template('machines.html',
                model=model, machines=machines, governorates=governorates, hospitals=hospitals)

@machinesbp.route('/models/<int:model_id>/add_machine', methods=['GET', 'POST'])
def add_machine(model_id):
    model = Model.query.get_or_404(model_id)
    form = MachineForm()
    name = 'Add'
    hospitals = Hospital.query.all()
    choises = [(hospital.id, hospital.name) for hospital in hospitals]
    form.hospital.choices = choises
    if form.validate_on_submit():
        machine = Machine(serial_number=form.serial_number.data,
                    model_id=model_id,
                    installation_date=form.installation_date.data,
                    contract_type=form.contract_type.data,
                    contract_name=form.contract_name.data,
                    contract_start_date=form.contract_start_date.data,
                    contract_end_date=form.contract_end_date.data,
                    hospital_id = form.hospital.data)
        db.session.add(machine)
        db.session.commit()
        flash(f'Machine  number {form.serial_number.data} for {model.name} {model.device.name} has been created successfully!', 'success')
        return redirect(url_for('machinesbp.machines', model_id=model_id))

    return render_template('add_machine.html', model=model, form=form, name=name)

@machinesbp.route('/machines/<int:machine_id>')
def machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    return render_template('machine.html', machine=machine)

@machinesbp.route('/delete_machine/<int:machine_id>', methods=['POST'])
def delete_machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    model = machine.model
    db.session.delete(machine)
    db.session.commit()
    flash(f'Machine {machine.serial_number} has been deleted successfully!', 'success')
    return redirect(url_for('machinesbp.machines', model_id=model.id))
    
@machinesbp.route('/update_machine/<int:machine_id>', methods=['GET', 'POST'])
def update_machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    form = MachineForm()
    name = 'Update'
    hospitals = Hospital.query.all()
    choises = [(hospital.id, hospital.name) for hospital in hospitals]
    form.hospital.choices = choises
    if form.validate_on_submit() or (request.method == 'POST' and form.serial_number.data == machine.serial_number):
        machine.serial_number = form.serial_number.data
        machine.installation_date = form.installation_date.data
        machine.contract_type = form.contract_type.data
        machine.contract_name = form.contract_name.data
        machine.contract_start_date = form.contract_start_date.data
        machine.contract_end_date = form.contract_end_date.data
        machine.hospital_id = form.hospital.data
        db.session.commit()
        flash('Machine has been updated successfully!', 'success')
        return redirect(url_for('machinesbp.machines', model_id=machine.model_id))
    form.serial_number.data = machine.serial_number
    form.installation_date.data = machine.installation_date
    form.contract_type.data = machine.contract_type
    form.contract_name.data = machine.contract_name
    form.contract_start_date.data = machine.contract_start_date
    form.contract_end_date.data = machine.contract_end_date
    form.submit.label.text = 'Update'
    return render_template('add_machine.html', form=form, machine=machine, name=name)