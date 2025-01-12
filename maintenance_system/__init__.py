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


from maintenance_system.Main import main
from maintenance_system.API import api
from maintenance_system.User import usersbp
from maintenance_system.Departments import departmentsbp
from maintenance_system.Devices import devicesbp
from maintenance_system.Model_of_machine import modelsbp
from maintenance_system.Machines import machinesbp
from maintenance_system.Hospitals import hospitalpb
from maintenance_system.Tasks import taskpb


app.register_blueprint(main)
app.register_blueprint(api)
app.register_blueprint(usersbp)
app.register_blueprint(departmentsbp)
app.register_blueprint(devicesbp)
app.register_blueprint(modelsbp)
app.register_blueprint(machinesbp)
app.register_blueprint(hospitalpb)
app.register_blueprint(taskpb)







