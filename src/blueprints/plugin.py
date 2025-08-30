from flask import render_template, Blueprint

from config.configuration import get_configuration_helper

plugin_bp = Blueprint("plugin", __name__)

@plugin_bp.route('/plugin/<plugin_name>')
def settings_page(plugin_name):   
    configuration = get_configuration_helper()
    plugin = configuration.get_plugin_by_name(plugin_name)
    return render_template("plugin.html", plugin_template=plugin.get_template())

def image()
