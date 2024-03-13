import os
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

# from flask_login import login_required


mappings_bp = Blueprint("mappings", __name__)


@mappings_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@mappings_bp.route("/mappings")
# @login_required
def index():
    return render_template("mappings/index.html")


@mappings_bp.route("/mappings/create")
# @login_required
def create():
    if "title" not in request.args:
        abort(404)

    title = request.args.get("title")
    return render_template("mappings/create.html", title=title)


@mappings_bp.route("/mappings", methods=["POST"])
def store():
    if "mapping-csv-input" not in request.files:
        flash("No file included")
        return redirect(request.url)
    file = request.files["mapping-csv-input"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file:
        # Save the mapping

        # TODO implement use case and infrastructure
        # title = request.form.get("title")
        # view_model = use_case(g.ctx, title, file)

        # Show the saved mapping
        return redirect(url_for("mappings.show"))
