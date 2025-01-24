import sys
import os
import unittest
from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from maintenance_system import db, bycrypt, login_manager 
from maintenance_system.models import Device
from flask import Flask
from maintenance_system.Devices import devicesbp


class TestUser(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.url_map.strict_slashes = False

        db.init_app(app)
        bycrypt.init_app(app)
        login_manager.init_app(app)
        app.register_blueprint(devicesbp)

        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_device(self):
        device = Device(name='X-Ray Machine', department_id=1)
        db.session.add(device)
        db.session.commit()
        devices = Device.query.all()
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].name, 'X-Ray Machine')

    def test_device_repr(self):
        device = Device(name='X-Ray Machine', department_id=1)
        self.assertEqual(str(device), '<Device: X-Ray Machine>')

    def test_device_delete(self):
        device = Device(name='X-Ray Machine', department_id=1)
        db.session.add(device)
        db.session.commit()
        devices = Device.query.all()
        self.assertEqual(len(devices), 1)
        db.session.delete(device)
        db.session.commit()
        devices = Device.query.all()
        self.assertEqual(len(devices), 0)

    def test_device_update(self):
        device = Device(name='X-Ray Machine', department_id=1)
        db.session.add(device)
        db.session.commit()
        devices = Device.query.all()
        self.assertEqual(len(devices), 1)
        device.name = 'MRI Machine'
        db.session.commit()
        devices = Device.query.all()
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].name, 'MRI Machine')

if __name__ == '__main__':
    unittest.main()