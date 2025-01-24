import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from maintenance_system import db, app
from maintenance_system.models import Hospital
import unittest
from flask_testing import TestCase

class TestHospital(TestCase):
	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

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