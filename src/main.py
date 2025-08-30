import json
import os
from flask import Flask
from blueprints.index import main_bp
from plugins.plugin import Plugin
from config.configuration import Configuration

json_config = os.path.join(os.path.dirname(__file__), "config", "config.json")
configuration = Configuration()

app = Flask(__name__)

def read_json_config():
    registered_plugin_names = []
    with open(json_config, "r") as file:
        data = json.load(file)
        registered_plugin_names = data["registered_plugins"]

    for plugin_name in registered_plugin_names:
        configuration.add_plugin(Plugin(plugin_name))
        
def register_blueprints():
    app.register_blueprint(main_bp)

def startup():
    app.config["Configuration"] = configuration
    read_json_config()
    register_blueprints()

def main():
    startup()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

