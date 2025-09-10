import os
from flask import current_app, jsonify, render_template, request, send_from_directory, Blueprint

from utils.plugin_utils import get_plugin_instance_by_config
from utils.task import ManualRefreshTask

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "..", "plugins")

plugin_bp = Blueprint("plugin", __name__)
    
@plugin_bp.route('/plugin/<plugin_id>')
def settings_page(plugin_id):
    app_config = current_app.config["Configuration"]
    plugin_config = app_config.get_plugin_config(plugin_id)
    plugin_instance = get_plugin_instance_by_config(plugin_config)
    template = plugin_instance.get_settings_template()
    return render_template("plugin.html", plugin=plugin_config, template=template)

@plugin_bp.route('/image/<plugin_id>')
def icon(plugin_id):
    plugin_dir = os.path.join(PLUGIN_DIR, plugin_id)
    return send_from_directory(plugin_dir, "icon.svg")

@plugin_bp.route('/submit_data/<plugin_id>', methods=['POST'])
def submit_data(plugin_id):
    payload = request.get_json()
    print("Received JSON:", payload)
    
    ManualRefreshTask(plugin_id, payload)
    return jsonify(success=True, received=payload)
