from flask import render_template
from maintenance_system import app


@app.route("/")
def home():
	return render_template("home.html")