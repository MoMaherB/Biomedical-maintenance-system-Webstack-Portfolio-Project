from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_system.db'
app.url_map.strict_slashes = False


db = SQLAlchemy(app)
bycrypt = Bcrypt(app)
login_manager = LoginManager(app)

from maintenance_system import routes

from maintenance_system.API.api import api
app.register_blueprint(api)


from maintenance_system.TheRoutes.departments_routes import departmentsbp
app.register_blueprint(departmentsbp)

from maintenance_system.TheRoutes.devices_routes import devicesbp
app.register_blueprint(devicesbp)


from maintenance_system.TheRoutes.models_routes import modelsbp
app.register_blueprint(modelsbp)

from maintenance_system.TheRoutes.machines_routes import machinesbp
app.register_blueprint(machinesbp)


from maintenance_system.TheRoutes.hospital_routes import hospitalpb
app.register_blueprint(hospitalpb)

from maintenance_system.TheRoutes.task_routes import taskpb
app.register_blueprint(taskpb)


