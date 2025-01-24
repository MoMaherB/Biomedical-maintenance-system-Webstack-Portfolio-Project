import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from maintenance_system import db, app
from maintenance_system.models import Department
import unittest
from flask_testing import TestCase

class TestDepartment(TestCase):
	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.drop_all()

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