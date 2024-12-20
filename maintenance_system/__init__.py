from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_system.db'
app.url_map.strict_slashes = False


db = SQLAlchemy(app)

from maintenance_system import routes