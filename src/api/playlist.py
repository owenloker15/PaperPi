import json
from datetime import timedelta

from flask import Blueprint, current_app, jsonify, render_template, request

from utils.app_utils import parse_form

playlist_bp = Blueprint("playlist", __name__)


@playlist_bp.route("/playlist")
def index():
    app_config = current_app.config["Configuration"]
    return render_template("playlist.html", plugins=app_config.get_plugin_configs())


@playlist_bp.route("/playlist/settings")
def get_playlist_settings():
    playlist = current_app.config["Playlist"]
    settings = playlist.get_playlist_settings_for_all()
    return jsonify(success=True, settings=settings)


@playlist_bp.route("/playlist/<plugin_id>/refresh", methods=["POST"])
def update_plugin_refresh(plugin_id):
    payload = request.get_json()

    playlist = current_app.config["Playlist"]
    playlist.set_plugin_refresh_timing(plugin_id, payload)

    return jsonify(success=True, received=payload)


@playlist_bp.route("/playlist/<plugin_id>/refresh")
def get_plugin_refresh(plugin_id):
    playlist = current_app.config["Playlist"]
    refresh_settings = playlist.get_plugin_refresh_timing(plugin_id)
    if refresh_settings is not None:
        return jsonify(success=True, refresh_settings=refresh_settings)
    else:
        return jsonify(success=False)


@playlist_bp.route("/playlist/<plugin_id>/schedule", methods=["POST"])
def update_plugin_schedule(plugin_id):
    payload = request.get_json()

    playlist = current_app.config["Playlist"]
    playlist.set_plugin_schedule(plugin_id, payload)

    return jsonify(success=True, received=payload)


@playlist_bp.route("/playlist/<plugin_id>/schedule")
def get_plugin_schedule(plugin_id):
    playlist = current_app.config["Playlist"]
    plugin_schedule = playlist.get_plugin_schedule(plugin_id)
    if plugin_schedule is not None:
        return jsonify(success=True, plugin_schedule=plugin_schedule)
    else:
        return jsonify(success=False)
