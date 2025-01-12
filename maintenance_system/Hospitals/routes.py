from flask import render_template, redirect, url_for, flash, request, Blueprint
from maintenance_system import db
from maintenance_system.models import Hospital
from .forms import HospitalForm

hospitalpb = Blueprint('hospitalpb', __name__)



@hospitalpb.route('/hospitals')
def hospitals():
    hospitals = Hospital.query.all()
    return render_template('hospitals.html', hospitals=hospitals)

@hospitalpb.route('/hospitals/<int:id>')
def hospital(id):
    hospital = Hospital.query.get_or_404(id)
    return render_template('hospital.html', hospital=hospital)

@hospitalpb.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    form_name = 'Add'
    form = HospitalForm()
    if form.validate_on_submit():
        hospital = Hospital(name=form.name.data, governorate=form.governorate.data.capitalize().strip())
        db.session.add(hospital)
        db.session.commit()
        flash('Hospital has been created successfully!', 'success')
        return redirect(url_for('hospitalpb.hospitals'))
    return render_template('add_hospital.html', form=form, form_name=form_name)

@hospitalpb.route('/delete_hospital/<int:id>', methods=['POST'])
def delete_hospital(id):
    hospital = Hospital.query.get_or_404(id)
    db.session.delete(hospital)
    db.session.commit()
    flash(f'Hospital {hospital.name} has been deleted successfully!', 'success')
    return redirect(url_for('hospitalpb.hospitals'))

@hospitalpb.route('/update_hospital/<int:id>', methods=['GET', 'POST'])
def update_hospital(id):
    hospital = Hospital.query.get_or_404(id)
    form_name = 'Update'
    form = HospitalForm()
    if form.validate_on_submit() or (request.method == 'POST' and form.name.data == hospital.name):
        hospital.name = form.name.data
        hospital.governorate = form.governorate.data.capitalize().strip()
        db.session.commit()
        flash('Hospital has been updated successfully!', 'success')
        return redirect(url_for('hospitalpb.hospitals'))
    form.name.data = hospital.name
    form.governorate.data = hospital.governorate
    form.submit.label.text = 'Update'
    return render_template('add_hospital.html', form=form, form_name=form_name)
