import sys
import os
import unittest
from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from maintenance_system import db, bycrypt, login_manager
from maintenance_system.models import Hospital
from flask import Flask
from maintenance_system.Hospitals import hospitalpb


class TestUser(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.url_map.strict_slashes = False

        db.init_app(app)
        bycrypt.init_app(app)
        login_manager.init_app(app)
        app.register_blueprint(hospitalpb)

        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_hospital(self):
        hospital = Hospital(name='Cairo Hospital', governorate='Cairo')
        db.session.add(hospital)
        db.session.commit()
        hospitals = Hospital.query.all()
        self.assertEqual(len(hospitals), 1)
        self.assertEqual(hospitals[0].name, 'Cairo Hospital')
        self.assertEqual(hospitals[0].governorate, 'Cairo')

    def test_hospital_repr(self):
        hospital = Hospital(name='Cairo Hospital', governorate='Cairo')
        self.assertEqual(str(hospital), '<Hospital: Cairo Hospital>')

    def test_hospital_delete(self):
        hospital = Hospital(name='Cairo Hospital', governorate='Cairo')
        db.session.add(hospital)
        db.session.commit()
        hospitals = Hospital.query.all()
        self.assertEqual(len(hospitals), 1)
        db.session.delete(hospital)
        db.session.commit()
        hospitals = Hospital.query.all()
        self.assertEqual(len(hospitals), 0)

    def test_hospital_update(self):
        hospital = Hospital(name='Cairo Hospital', governorate='Cairo')
        db.session.add(hospital)
        db.session.commit()
        hospitals = Hospital.query.all()
        self.assertEqual(len(hospitals), 1)
        hospital.name = 'Giza Hospital'
        hospital.governorate = 'Giza'
        db.session.commit()
        hospitals = Hospital.query.all()
        self.assertEqual(len(hospitals), 1)
        self.assertEqual(hospitals[0].name, 'Giza Hospital')
        self.assertEqual(hospitals[0].governorate, 'Giza')

if __name__ == '__main__':
    unittest.main()