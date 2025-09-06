import json
import os
from flask import Flask
from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from blueprints.index import main_bp
from blueprints.plugin import plugin_bp
from configuration import Configuration
from utils.plugin_utils import load_plugins

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

app_config = Configuration()

app = Flask(__name__)

template_dirs = [
   os.path.join(os.path.dirname(__file__), "templates"),    # Default template folder
   os.path.join(os.path.dirname(__file__), "plugins"),      # Plugin templates
]
app.jinja_loader = ChoiceLoader([FileSystemLoader(directory) for directory in template_dirs])

def register_blueprints():
    app.register_blueprint(main_bp)
    app.register_blueprint(plugin_bp)

def startup():
    load_plugins(app_config.get_plugin_configs())
    app.config["Configuration"] = app_config
    register_blueprints()

def main():
    startup()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

