from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    return redirect(url_for('usersbp.login'))


@main.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return f"Caught route: {path}", 404
