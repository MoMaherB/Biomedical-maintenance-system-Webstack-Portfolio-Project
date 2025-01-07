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

