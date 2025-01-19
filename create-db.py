from maintenance_system import db, app
from maintenance_system.models import User, Department, Hospital
from flask_bcrypt import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    print("Database created")
    hash_password = generate_password_hash("Adminpassword").decode('utf-8')
    admin = User(username="Admin", email="ff@gmal.com", password=hash_password, rank="Senior")

    db.session.add(admin)
    db.session.commit()
    all = User.query.all()
    print("Users added to the database")