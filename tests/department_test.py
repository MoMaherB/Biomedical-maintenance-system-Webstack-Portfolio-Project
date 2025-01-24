import sys
import os
import unittest
from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from maintenance_system import db, bycrypt, login_manager 
from maintenance_system.models import Department
from flask import Flask
from maintenance_system.Departments import departmentsbp


class TestUser(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.url_map.strict_slashes = False

        db.init_app(app)
        bycrypt.init_app(app)
        login_manager.init_app(app)
        app.register_blueprint(departmentsbp)

        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestUser(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.url_map.strict_slashes = False

        db.init_app(app)
        bycrypt.init_app(app)
        login_manager.init_app(app)
        app.register_blueprint(departmentsbp)

        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        

    def test_department(self):
        department = Department(name='Radiology')
        db.session.add(department)
        db.session.commit()
        departments = Department.query.all()
        self.assertEqual(len(departments), 1)
        self.assertEqual(departments[0].name, 'Radiology')

    def test_department_repr(self):
        department = Department(name='Radiology')
        self.assertEqual(str(department), '<Department: Radiology>')

    def test_department_delete(self):
        department = Department(name='Radiology')
        db.session.add(department)
        db.session.commit()
        departments = Department.query.all()
        self.assertEqual(len(departments), 1)
        db.session.delete(department)
        db.session.commit()
        departments = Department.query.all()
        self.assertEqual(len(departments), 0)

    def test_department_update(self):
        department = Department(name='Radiology')
        db.session.add(department)
        db.session.commit()
        departments = Department.query.all()
        self.assertEqual(len(departments), 1)
        department.name = 'Cardiology'
        db.session.commit()
        departments = Department.query.all()
        self.assertEqual(len(departments), 1)
        self.assertEqual(departments[0].name, 'Cardiology')

if __name__ == '__main__':
    unittest.main()