import sys
import os
import unittest
from flask_testing import TestCase

# Dynamically import the original package components
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from maintenance_system import db, bycrypt, login_manager  # These are just for reference, we're creating a new app instance
from maintenance_system.models import User
from flask import Flask
from maintenance_system.User import usersbp  # Import the User Blueprint


class TestUser(TestCase):
    def create_app(self):
        # Create a new Flask app instance for testing
        app = Flask(__name__)

        # Test configuration
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
        app.url_map.strict_slashes = False

        # Initialize extensions for the new app instance
        db.init_app(app)
        bycrypt.init_app(app)
        login_manager.init_app(app)
        # Register Blueprint for testing
        app.register_blueprint(usersbp)

        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        """Test creating a user"""
        user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')

        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'Mohamed Maher')
        self.assertEqual(users[0].email, 'mohamed@maher.com')

    def test_user_repr(self):
        """Test the string representation of a user"""
        user = User(username='Mohamed Maher', email='mohamed@maher.com', password='password123')
        self.assertEqual(str(user), '<User: Mohamed Maher> - Email: mohamed@maher.com, Rank: None')

    def test_user_delete(self):
        """Test deleting a user"""
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
        """Test updating a user's information"""
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
