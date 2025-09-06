import os
from flask import render_template, send_from_directory, Blueprint

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "..", "plugins")

plugin_bp = Blueprint("plugin", __name__)
    
@plugin_bp.route('/plugin/<plugin_id>')
def settings_page(plugin_id):
    return render_template(f"{plugin_id}/settings.html")

@plugin_bp.route('/image/<plugin_id>')
def icon(plugin_id):
    plugin_dir = os.path.join(PLUGIN_DIR, plugin_id)
    return send_from_directory(plugin_dir, "icon.svg")
