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
from nad_ch.application.use_cases.column_maps import add_column_map

mappings_bp = Blueprint("mappings", __name__)


@mappings_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@mappings_bp.route("/mappings")
@login_required
def index():
    return render_template("mappings/index.html")


@mappings_bp.route("/mappings/create")
@login_required
def create():
    if "title" not in request.args:
        abort(404)

    title = request.args.get("title")
    return render_template("mappings/create.html", title=title)


@mappings_bp.route("/mappings", methods=["POST"])
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
        title = request.form.get("title")
        view_model = add_column_map(g.ctx, current_user.id, title, file)
        return redirect(url_for("mappings.show", id=view_model.id))
