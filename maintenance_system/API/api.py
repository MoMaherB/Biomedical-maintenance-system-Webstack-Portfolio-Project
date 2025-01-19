from flask import request, jsonify, Blueprint
from maintenance_system import db
from maintenance_system.models import User, Department, Device, Hospital
from flask_bcrypt import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)


@api.post('/api/register')
def register():
    """Register a new user"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    exist_user = User.query.filter_by(email=data['email']).first()
    if exist_user:
        return jsonify({"message": f"User {data['email']} already exists!"}), 400
    user = User(username=data['username'], email=data['email'], rank=data['rank'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {data['username']} has been created successfully!"}), 201


@api.post('/api/login')
def login():
    """Login a user"""
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": f"User {user.username} has been logged in successfully!"}), 200


@api.get('/api/users')
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email, "rank": user.rank} for user in users])


@api.get('/api/users/<int:id>')
def get_user(id):
    """Get a user by id"""
    user = User.query.get_or_404(id)
    return jsonify({"id": id, "username": user.username, "email": user.email, "rank": user.rank})


@api.get('/api/departments')
def get_departments():
    """Get all departments"""
    departments = Department.query.all()
    return jsonify([{"id": department.id, "name": department.name} for department in departments])


@api.get('/api/departments/<int:id>')
def get_department(id):
    """Get a department by id"""
    department = Department.query.get_or_404(id)
    return jsonify({"id": id, "name": department.name})


@api.post('/api/departments')
def add_department():
    """Add a new department"""
    data = request.get_json()
    department = Department(name=data['name'])
    db.session.add(department)
    db.session.commit()
    return jsonify({"message": f"Department {data['name']} has been created successfully!"}), 201


@api.delete('/api/departments/<int:id>')
def delete_department(id):
    """Delete a department by id"""
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return jsonify({"message": f"Department {department.name} has been deleted successfully!"}), 200


@api.get('/api/departments/<int:department_id>/devices')
def get_devices(department_id):
    """Get all devices in a department"""
    department = Department.query.get_or_404(department_id)
    devices = department.devices
    return jsonify([{"id": device.id, "name": device.name} for device in devices])


@api.post('/api/departments/<int:department_id>/devices')
def add_device(department_id):
    """ Add a new device to a department"""
    data = request.get_json()
    device = Device(name=data['name'], department_id=department_id)
    db.session.add(device)
    db.session.commit()
    return jsonify({"message": f"Device {data['name']} has been created successfully!"}), 201


@api.get('/api/departments/<int:department_id>/devices/<int:device_id>')
def get_device(department_id, device_id):
    """Get a device by id"""
    device = Device.query.get_or_404(device_id)
    return jsonify({"id": device.id, "name": device.name, "department_id": department_id})


@api.delete('/api/departments/<int:department_id>/devices/<int:device_id>')
def delete_device(department_id, device_id):
    """Delete a device by id"""
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({"message": f"Device {device.name} has been deleted successfully!"}), 200


@api.get('/api/hospitals')
def hospitals():
    """Get all hospitals"""
    hospitals = Hospital.query.all()
    return jsonify([{"id": hospital.id, "name": hospital.name, "governorate": hospital.governorate} for hospital in hospitals])


@api.get('/api/hospitals/<int:id>')
def hospital(id):
    """Get a hospital by id"""
    hospital = Hospital.query.get_or_404(id)
    return jsonify({"id": hospital.id, "name": hospital.name, "governorate": hospital.governorate})
