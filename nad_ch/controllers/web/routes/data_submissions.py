from flask import (
    Blueprint,
    current_app,
    render_template,
    g,
    jsonify,
    request,
    abort,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from nad_ch.application.exceptions import (
    InvalidDataSubmissionFileError,
    InvalidSchemaError,
)
from nad_ch.application.use_cases.column_maps import get_column_maps_by_producer
from nad_ch.application.use_cases.data_submissions import (
    get_data_submission,
    get_data_submissions_by_producer,
    create_data_submission,
    validate_file_before_submission,
)


submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@submissions_bp.route("/data-submissions")
@login_required
def index():
    try:
        view_models = get_data_submissions_by_producer(
            g.ctx, current_user.producer.name
        )
        return render_template("data_submissions/index.html", submissions=view_models)
    except ValueError:
        abort(404)


@submissions_bp.route("/data-submissions/<id>")
@login_required
def show(id):
    try:
        view_model = get_data_submission(g.ctx, id)
        return render_template("data_submissions/show.html", submission=view_model)
    except Exception:
        abort(404)


@submissions_bp.route("/data-submissions/create")
@login_required
def create():
    if "name" not in request.args:
        abort(404)

    name = request.args.get("name")
    column_map_options = get_column_maps_by_producer(g.ctx, current_user.producer.name)
    return render_template(
        "data_submissions/create.html", name=name, column_map_options=column_map_options
    )


@submissions_bp.route("/data-submissions", methods=["POST"])
@login_required
def store():
    name = request.form.get("name")
    column_map_id = request.form.get("column-map-id")

    if not name:
        flash("Name is required")
        return redirect(url_for("submissions.create"))

    if "mapping-csv-input" not in request.files:
        flash("No file included")
        return redirect(url_for("submissions.create", name=name))

    file = request.files["mapping-csv-input"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("submissions.create", name=name))

    try:
        validate_file_before_submission(g.ctx, file, column_map_id)
    except InvalidDataSubmissionFileError as e:
        flash(f"Error: {e}")
        return redirect(url_for("submissions.create", name=name))
    except InvalidSchemaError as e:
        flash(f"Error: {e}")
        return redirect(url_for("submissions.create", name=name))

    try:
        view_model = create_data_submission(
            g.ctx, current_user.id, column_map_id, name, file
        )

        return redirect(url_for("submissions.edit", id=view_model.id))
    except ValueError as e:
        flash(f"Error: {e}")
        return redirect(url_for("submissions.create", name=name))


@submissions_bp.route("/data-submissions/edit/<id>")
@login_required
def edit(id):
    try:
        view_model = get_data_submission(g.ctx, id)

        data = [
            {
                "Add_Number": "34",
                "St_Name": "Willow Creek Blvd",
                "Latitude": "44.968046",
                "Longitude": "-94.420307",
            },
            {
                "Add_Number": "654",
                "St_Name": "Pinehurst Lane",
                "Latitude": "33.755787",
                "Longitude": "-89.132008",
            },
            {
                "Add_Number": "324",
                "St_Name": "Cedarwood Drive",
                "Latitude": "33.844843",
                "Longitude": "-116.359998",
            },
            {
                "Add_Number": "43",
                "St_Name": "Mapleview Court",
                "Latitude": "44.92057",
                "Longitude": "-116.54911",
            },
            {
                "Add_Number": "5",
                "St_Name": "Elm Street",
                "Latitude": "44.240309",
                "Longitude": "-93.44786",
            },
            {
                "Add_Number": "545",
                "St_Name": "Oak Ridge Way",
                "Latitude": "44.968041",
                "Longitude": "-91.493619",
            },
            {
                "Add_Number": "34",
                "St_Name": "Sunnybrook Road",
                "Latitude": "44.333304",
                "Longitude": "-94.419696",
            },
            {
                "Add_Number": "4",
                "St_Name": "Riverside Terrace",
                "Latitude": "33.755783",
                "Longitude": "-89.132027",
            },
            {
                "Add_Number": "34",
                "St_Name": "Meadowbrook Lane",
                "Latitude": "33.844847",
                "Longitude": "-116.360066",
            },
            {
                "Add_Number": "34",
                "St_Name": "Aspen Grove Circle",
                "Latitude": "44.920474",
                "Longitude": "-116.549069",
            },
        ]

        return render_template(
            "data_submissions/edit.html", submission=view_model, data=data
        )
    except Exception:
        abort(404)


@submissions_bp.route("/api/reports/<submission_id>")
@login_required
def view_report_json(submission_id):
    view_model = get_data_submission(g.ctx, submission_id)
    return jsonify(view_model.report)
