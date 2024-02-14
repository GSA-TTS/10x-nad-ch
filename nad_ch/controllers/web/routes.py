from flask import Blueprint, current_app, render_template, g
from nad_ch.application.use_cases import (
    list_data_submissions_by_producer,
    get_data_submission,
)


home_bp = Blueprint("home", __name__)


@home_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@home_bp.route("/")
def home():
    return render_template("index.html")


@home_bp.route("/reports")
def reports():
    # For demo purposes, hard-code the producer name
    view_model = list_data_submissions_by_producer(g.ctx, "NJ")
    return render_template("reports/index.html", submissions=view_model)


@home_bp.route("/reports/<submission_id>")
def view_report(submission_id):
    view_model = get_data_submission(g.ctx, submission_id)
    return render_template("reports/show.html", submission=view_model)
