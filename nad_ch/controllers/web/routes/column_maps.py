import csv
import io
from flask import (
    Blueprint,
    current_app,
    render_template,
    g,
    request,
    abort,
    redirect,
    flash,
    url_for,
)
from flask_login import login_required, current_user
from nad_ch.application.use_cases.column_maps import (
    add_column_map,
    get_column_map,
    get_column_maps_by_producer,
    update_column_mapping,
    update_column_mapping_field,
)


column_maps_bp = Blueprint("column_maps", __name__)


@column_maps_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@column_maps_bp.route("/column-maps")
@login_required
def index():
    try:
        view_models = get_column_maps_by_producer(g.ctx, "New Jersey")
        return render_template("column_maps/index.html", column_maps=view_models)
    except ValueError:
        abort(404)


@column_maps_bp.route("/column-maps/create")
@login_required
def create():
    if "name" not in request.args:
        abort(404)

    name = request.args.get("name")
    return render_template("column_maps/create.html", name=name)


@column_maps_bp.route("/column-maps", methods=["POST"])
@login_required
def store():
    if request.form.get("_method") == "PUT":
        return update(request)

    if "mapping-csv-input" not in request.files:
        flash("No file included")
        return redirect(url_for("column_maps.create"))

    file = request.files["mapping-csv-input"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("column_maps.create"))

    try:
        file_content = file.read().decode("utf-8-sig")
        stream = io.StringIO(file_content)
        csv_reader = csv.reader(stream, dialect="excel")

        headers = next(csv_reader)
        if not headers:
            flash("CSV file seems to be empty or invalid")
            return redirect(url_for("column_maps.create"))

        csv_dict = {}

        for row in csv_reader:
            if len(row) < 2:
                continue
            key, value = row[:2]
            csv_dict[key] = value

    except Exception as e:
        flash(f"An error occurred while processing the file: {e}")
        return redirect(url_for("column_maps.create"))

    try:
        name = request.form.get("name")
        view_model = add_column_map(g.ctx, current_user.id, name, csv_dict)
        return redirect(url_for("column_maps.show", id=view_model.id))
    except ValueError as e:
        flash(f"Error: {e}")
        return redirect(url_for("column_maps.create"))


@column_maps_bp.route("/column-maps/update/<id>", methods=["POST"])
@login_required
def update(id):
    if request.form.get("_formType") == "existing_fields":
        excluded_form_keys = ("_method", "_formType", "_id")

        mapping = {
            key: value
            for key, value in request.form.items()
            if key not in excluded_form_keys
        }

        try:
            view_model = update_column_mapping(g.ctx, id, mapping)
            return redirect(url_for("column_maps.show", id=view_model.id))
        except ValueError:
            flash("Error: ", str(ValueError))
            return redirect(url_for("column_maps.edit", id=id))
    elif request.form.get("_formType") == "new_field":
        user_field = request.form.get("newField")
        nad_field = request.form.get("newNadField")
        try:
            view_model = update_column_mapping_field(g.ctx, id, user_field, nad_field)
            return redirect(url_for("column_maps.show", id=view_model.id))
        except ValueError:
            flash("Error: ", str(ValueError))
            return redirect(url_for("column_maps.edit", id=id))
    else:
        abort(404)


@column_maps_bp.route("/column-maps/<id>")
@login_required
def show(id):
    try:
        view_model = get_column_map(g.ctx, id)
        return render_template("column_maps/show.html", column_map=view_model)
    except ValueError:
        abort(404)


@column_maps_bp.route("/column-maps/edit/<id>")
@login_required
def edit(id):
    try:
        view_model = get_column_map(g.ctx, id)
        return render_template("column_maps/edit.html", column_map=view_model)
    except Exception:
        abort(404)
