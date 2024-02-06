from flask import Blueprint, current_app, render_template, g


home_bp = Blueprint("home", __name__)


@home_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@home_bp.route("/")
def home():
    return render_template("index.html")


@home_bp.route("/reports")
def reports():
    return render_template("reports.html")
