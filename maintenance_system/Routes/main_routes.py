from flask import render_template
from maintenance_system import app


@app.route("/")
def home():
    return render_template("home.html")

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return f"Caught route: {path}", 404
