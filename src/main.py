import json
import os
from flask import Flask
from blueprints.index import main_bp

json_config = os.path.join(os.path.dirname(__file__), "config", "config.json")

app = Flask(__name__)

def read_json_config():
    with open(json_config, "r") as file:
        data = json.load(file)
        app.config["REGISTERED_PLUGINS"] = data["registered_plugins"]

def register_blueprints():
    app.register_blueprint(main_bp)

def startup():
    read_json_config()
    register_blueprints()

def main():
    startup()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

