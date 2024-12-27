from maintenance_system import db, app
from maintenance_system.models import User, Department, Hospital

with app.app_context():
    db.drop_all()
    db.create_all()

    print("Database created")
    user1 = User(username="Maher", email="ff@gmal.com", password="password", rank="Senior")
    user2 = User(username="Ali", email="fvf@gmal.com", password="password", rank="Senior")
    user3 = User(username="Amgad", email="dd@gmal.com", password="password", rank="Senior")
    user4 = User(username="Motaz", email="ss@gmal.com", password="password", rank="Senior")
    user5 = User(username="Mustafa", email="Mus@gmal.com", password="password", rank="Senior")
    hospital = Hospital(name="Dar Elshefaa", governorate="Cairo")
    hospita2 = Hospital(name="Nile Badrawy", governorate="Cairo")
    hospita3 = Hospital(name="Hawamdia", governorate="Giza")
    hospita4 = Hospital(name="Elmounira", governorate="Giza")

    department1 = Department(name = "Criticl Care", members=[user1, user2, user3])
    department2 = Department(name = "SW", members=[user4, user5])

    db.session.add_all([user1, user2, user3, user4, user5, department1, department2, hospital, hospita2, hospita3, hospita4])
    db.session.commit()
    all = User.query.all()
    print("Users added to the database")

    for user in all:
        print(user)