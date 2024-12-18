from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_system.db'
db = SQLAlchemy(app)

from maintenance_system import routes