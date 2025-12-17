from flask import Blueprint, current_app, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    app_config = current_app.config["Configuration"]
    playlist = current_app.config["Playlist"]
    return render_template(
        "index.html",
        plugins=app_config.get_plugin_configs(),
        active_plugin=app_config.get_plugin_config(playlist.get_active_plugin_id()),
    )
