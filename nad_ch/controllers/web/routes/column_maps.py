import csv
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
    if "mapping-csv-input" not in request.files:
        flash("No file included")
        return redirect(url_for("column_maps.create"))

    file = request.files["mapping-csv-input"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("column_maps.create"))

    if not file.filename.endswith('.csv'):
        flash("File is not a CSV")
        return redirect(url_for("column_maps.create"))

    if file:
        csv_dict = {}

        try:
            file_content = file.read().decode("utf-8").splitlines()
            csv_reader = csv.reader(file_content)

            for row in csv_reader:
                key, value = row
                csv_dict[key] = value

        except Exception as e:
            flash(f"An error occurred while processing the file: {e}")
            return redirect(url_for("column_maps.create"))


        try:
            name = request.form.get("name")
            view_model = add_column_map(g.ctx, current_user.id, name, csv_dict)
            return redirect(url_for("column_maps.show", id=view_model.id))
        except ValueError:
            flash("Error: ", str(ValueError))
            return redirect(url_for("column_maps.create"))

@column_maps_bp.route("/column-maps/<id>")
@login_required
def show(id):
    try:
        view_model = get_column_map(g.ctx, id)
        return render_template("column_maps/show.html", column_map=view_model)
    except ValueError:
        abort(404)
