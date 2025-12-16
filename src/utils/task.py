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

            # Get next active plugin
            next_active_plugin_id, schedule_time_delta = next_active_plugin(
                self.playlist, app
            )

            print(f"Active Plugin: ", active_plugin_id)
            print(f"Next Plugin: ", next_active_plugin_id)
            if active_plugin_id is not None:
                plugin_instance = get_plugin_instance_by_id(active_plugin_id)
                plugin_instance.render_image(app)
                refresh_settings = self.playlist.get_plugin_refresh_timing(
                    active_plugin_id
                )
                refresh_time_delta = json_to_timedelta(refresh_settings)

                # If the next trigger event is a plugin change, change the active plugin then sleep
                # else, just sleep till next refresh.
                if next_active_plugin_id is not None:
                    if schedule_time_delta < refresh_time_delta:
                        self.playlist.set_active_plugin_id(next_active_plugin_id)
                        time.sleep(schedule_time_delta.total_seconds())
                    else:
                        time.sleep(refresh_time_delta.total_seconds())
                else:
                    time.sleep(refresh_time_delta.total_seconds())
            else:
                print("No active plugin set!")


class TaskManager:
    def __init__(self):
        self.activeTasks: list[BaseTask] = []

    def submit_task(self, task: BaseTask):
        task.start()
