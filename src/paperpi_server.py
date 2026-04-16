import os

from dotenv import load_dotenv
from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from flask_socketio import SocketIO  # Add socketio

from api.index import main_bp
from api.playlist import playlist_bp
from api.plugin import plugin_bp
from configuration import Configuration
from display.display_manager import DisplayManager
from utils.playlist import Playlist
from utils.plugin_utils import load_plugins
from utils.task import BackgroundRefreshTask, TaskManager

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

app_config = Configuration()
task_manager = TaskManager()
display_manager = DisplayManager()
playlist = Playlist()
socketio = SocketIO(app, cors_allowed_origins="*")  # add socketio

app = Flask(__name__)


template_dirs = [
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__), "plugins"),
]

app.jinja_loader = ChoiceLoader(
    [FileSystemLoader(directory) for directory in template_dirs]
)


def register_blueprints():
    app.register_blueprint(main_bp)
    app.register_blueprint(plugin_bp)
    app.register_blueprint(playlist_bp)


def startup():
    load_plugins(app_config.get_plugin_configs())

    app.config["Configuration"] = app_config
    app.config["Task_Manager"] = task_manager
    app.config["Display_Manager"] = display_manager
    app.config["Playlist"] = playlist
    app.config["socketio"] = socketio  # add socketio

    register_blueprints()

    task = BackgroundRefreshTask(app)
    task_manager.submit_task(task)


def main():
    startup()
    port = os.getenv("PORT")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
