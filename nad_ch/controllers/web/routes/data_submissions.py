from flask import Blueprint, current_app, render_template, g, jsonify
from flask_login import login_required, current_user
from nad_ch.application.use_cases.data_submissions import (
    get_data_submission,
    list_data_submissions_by_producer,
)


submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@submissions_bp.route("/data-submissions")
@login_required
def index():
    pass


@submissions_bp.route("/data-submissions/<submission_id>")
@login_required
def show(submission_id):
    pass


@submissions_bp.route("/reports")
@login_required
def reports():
    # For demo purposes, hard-code the producer name
    view_model = list_data_submissions_by_producer(g.ctx, current_user.producer.name)
    return render_template("data_submissions/index.html", submissions=view_model)


@submissions_bp.route("/reports/<submission_id>")
@login_required
def view_report(submission_id):
    view_model = get_data_submission(g.ctx, submission_id)
    return render_template("data_submissions/show.html", submission=view_model)


@submissions_bp.route("/api/reports/<submission_id>")
@login_required
def view_report_json(submission_id):
    view_model = get_data_submission(g.ctx, submission_id)
    return jsonify(view_model.report)
