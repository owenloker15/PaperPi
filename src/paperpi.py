import json
import os
from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from blueprints.index import main_bp
from blueprints.plugin import plugin_bp
from plugins.plugin import Plugin
from config.configuration import Configuration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

json_config = os.path.join(BASE_DIR, "config", "config.json")
app_config = Configuration()

app = Flask(__name__)
template_dirs = [
   os.path.join(os.path.dirname(__file__), "templates"),    # Default template folder
   os.path.join(os.path.dirname(__file__), "plugins", "weather"),      # Plugin templates
]

print(template_dirs)
app.jinja_loader = ChoiceLoader([FileSystemLoader(template_dirs + os.listdir(directory)) for directory in template_dirs])

def read_json_config():
    registered_plugin_names = []
    with open(json_config, "r") as file:
        data = json.load(file)
        registered_plugin_names = data["registered_plugins"]

    for plugin_name in registered_plugin_names:
        app_config.add_plugin(Plugin(plugin_name))
        
def register_blueprints():
    app.register_blueprint(main_bp)
    app.register_blueprint(plugin_bp)

def startup():
    app.config["Configuration"] = app_config
    read_json_config()
    register_blueprints()

def main():
    startup()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

