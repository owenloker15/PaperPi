from flask import current_app, render_template, Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    registered_plugins = current_app.config["REGISTERED_PLUGINS"]
    return render_template("index.html", plugins=registered_plugins)
