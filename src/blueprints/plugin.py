from flask import render_template, send_from_directory, Blueprint, current_app

from config.configuration import Configuration

plugin_bp = Blueprint("plugin", __name__)
    
@plugin_bp.route('/plugin/<plugin_name>')
def settings_page(plugin_name):
    app_config = current_app.config["Configuration"]
    plugin = app_config.get_plugin_by_name(plugin_name)
    return render_template(plugin.get_template())
    # return "Random string!"

@plugin_bp.route('/image/<plugin_name>')
def icon(plugin_name):
    app_config = current_app.config["Configuration"]
    plugin = app_config.get_plugin_by_name(plugin_name)
    return send_from_directory("icon.png")
