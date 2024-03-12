from flask import Blueprint, current_app, render_template, g, request, abort

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
