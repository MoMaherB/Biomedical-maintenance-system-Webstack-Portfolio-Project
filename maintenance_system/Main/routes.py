from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return f"Caught route: {path}", 404
