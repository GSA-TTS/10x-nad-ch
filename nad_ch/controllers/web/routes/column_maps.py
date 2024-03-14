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
from nad_ch.application.use_cases.column_maps import add_column_map, get_column_map, get_column_maps_by_provider


column_maps_bp = Blueprint("column_maps", __name__)


@column_maps_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@column_maps_bp.route("/column-maps")
@login_required
def index():
    view_models = get_column_maps_by_provider(g.ctx, 1)
    return render_template("column_maps/index.html", column_maps=view_models)


@column_maps_bp.route("/column-maps/create")
@login_required
def create():
    if "name" not in request.args:
        abort(404)

    name = request.args.get("name")
    return render_template("column-maps/create.html", name=name)


@column_maps_bp.route("/column-maps", methods=["POST"])
@login_required
def store():
    if "mapping-csv-input" not in request.files:
        flash("No file included")
        return redirect(request.url)
    file = request.files["mapping-csv-input"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file:
        name = request.form.get("name")
        content = file.read()
        mapping_string = content.decode('utf-8')

        view_model = add_column_map(g.ctx, current_user.id, name,  mapping_string)

        return redirect(url_for("column_maps/show.html", column_map=view_model))


@column_maps_bp.route("/column-maps/<mapping_id>")
@login_required
def show(mapping_id):
    view_model = get_column_map(g.ctx, mapping_id)
    return render_template("column_maps/show.html", column_map=view_model)
