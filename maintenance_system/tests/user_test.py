import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from maintenance_system import db, app
from maintenance_system.models import User
import unittest
from flask_testing import TestCase

class TestUser(TestCase):
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

	def test_user(self):
		user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')
		db.session.add(user)
		db.session.commit()
		users = User.query.all()
		self.assertEqual(len(users), 1)
		self.assertEqual(users[0].username, 'Mohamed Maher')
		self.assertEqual(users[0].email, 'mohamed@maher.com')

	def test_user_repr(self):
		user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')
		self.assertEqual(str(user), '<User: Mohamed Maher> - Email: mohamed@maher.com, Rank: None')

	def test_user_delete(self):
		user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')
		db.session.add(user)
		db.session.commit()
		users = User.query.all()
		self.assertEqual(len(users), 1)
		db.session.delete(user)
		db.session.commit()
		users = User.query.all()
		self.assertEqual(len(users), 0)

	def test_user_update(self):
		user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')
		db.session.add(user)
		db.session.commit()
		users = User.query.all()
		self.assertEqual(len(users), 1)
		user.username = 'jane_doe'
		user.email = 'jane@example.com'
		db.session.commit()
		users = User.query.all()
		self.assertEqual(len(users), 1)
		self.assertEqual(users[0].username, 'jane_doe')
		self.assertEqual(users[0].email, 'jane@example.com')

if __name__ == '__main__':
	unittest.main()