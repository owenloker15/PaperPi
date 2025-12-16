import threading
import time
from datetime import datetime, timedelta

from utils.app_utils import json_to_timedelta, next_active_plugin
from utils.plugin_utils import get_plugin_instance_by_id


class BaseTask:
    def start(self):
        pass

    def stop(self):
        pass

    def onComplete(self, callback=None):
        if callback is not None:
            callback()

    def _run(self, app):
        pass


class ManualRefreshTask(BaseTask):
    def __init__(self, plugin_id, plugin_settings, app):
        self.plugin_id = plugin_id
        self.plugin_settings = plugin_settings

        self.thread = threading.Thread(target=self._run, args=(app,), daemon=True)

    def start(self):
        self.thread.start()

    def _run(self, app):
        plugin_instance = get_plugin_instance_by_id(self.plugin_id)
        plugin_instance.save_settings(self.plugin_settings)
        playlist = app.config["Playlist"]
        playlist.set_active_plugin_id(self.plugin_id)
        return plugin_instance.render_image(app)


class BackgroundRefreshTask(BaseTask):
    def __init__(self, app):
        self.running = False
        self.thread = threading.Thread(target=self._run, args=(app,), daemon=True)
        self.playlist = app.config["Playlist"]

    def start(self):
        if not self.running:
            self.running = True
            self.thread.start()
        else:
            print("Thread already running!")

    def stop(self):
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
        else:
            print("Thread is not running!")

    def _run(self, app):
        while self.running:
            active_plugin_id = self.playlist.get_active_plugin_id()
            next_plugin_id, schedule_delta = next_active_plugin(self.playlist, app)

            print(f"Active Plugin: {active_plugin_id}")
            print(f"Next Plugin: {next_plugin_id}")

            refresh_delta = timedelta()

            # Determine refresh timing
            if active_plugin_id is not None:
                refresh_settings = self.playlist.get_plugin_refresh_timing(
                    active_plugin_id
                )
                refresh_delta = json_to_timedelta(refresh_settings)

            # Possible events:
            # 1) Refresh active plugin
            # 2) Switch to next scheduled plugin
            # 3) Idle (nothing configured)

            # Case: no active plugin AND no scheduled plugin
            if active_plugin_id is None and next_plugin_id is None:
                print("No active or scheduled plugin. Sleeping briefly.")
                time.sleep(1)
                continue

            # Case: active plugin exists → render immediately
            if active_plugin_id is not None:
                plugin_instance = get_plugin_instance_by_id(active_plugin_id)
                plugin_instance.render_image(app)

            # Case: only scheduled plugin exists (no active yet)
            if active_plugin_id is None and next_plugin_id is not None:
                print("Waiting for scheduled plugin to become active.")
                time.sleep(schedule_delta.total_seconds())
                self.playlist.set_active_plugin_id(next_plugin_id)
                continue

            # Case: active exists but no scheduled plugin
            if active_plugin_id is not None and next_plugin_id is None:
                time.sleep(refresh_delta.total_seconds())
                continue

            # Case: both active and scheduled plugins exist
            # Choose the earlier event
            if schedule_delta < refresh_delta:
                # Plugin switch happens first
                time.sleep(schedule_delta.total_seconds())
                self.playlist.set_active_plugin_id(next_plugin_id)
            else:
                # Refresh happens first
                time.sleep(refresh_delta.total_seconds())


class TaskManager:
    def __init__(self):
        self.activeTasks: list[BaseTask] = []

    def submit_task(self, task: BaseTask):
        task.start()
