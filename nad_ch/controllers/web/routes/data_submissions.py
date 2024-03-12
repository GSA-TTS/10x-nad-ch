from flask import Blueprint, current_app, render_template, g
from flask_login import login_required
from nad_ch.application.use_cases.data_submissions import (
    get_data_submission,
    list_data_submissions_by_producer,
)


submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@submissions_bp.route("/reports")
@login_required
def reports():
    # For demo purposes, hard-code the producer name
    view_model = list_data_submissions_by_producer(g.ctx, "New Jersey")
    return render_template("data_submissions/index.html", submissions=view_model)


@submissions_bp.route("/reports/<submission_id>")
@login_required
def view_report(submission_id):
    view_model = get_data_submission(g.ctx, submission_id)
    return render_template("data_submissions/show.html", submission=view_model)
