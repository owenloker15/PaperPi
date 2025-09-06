from flask import render_template, Blueprint, current_app

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    app_config = current_app.config["Configuration"]
    print(app_config.get_plugin_configs())
    return render_template("index.html", plugins=app_config.get_plugin_configs())
    
