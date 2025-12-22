import threading
import time
from datetime import datetime, timedelta

from utils.app_utils import json_to_timedelta, next_active_plugin
from utils.plugin_utils import get_plugin_instance_by_id

def sleep_interruptible(stop_event: threading.Event, seconds: float) -> bool:
    """
    Sleeps for `seconds` unless stop_event is set.
    Returns False if interrupted, True if completed.
    """
    end = time.monotonic() + seconds
    while not stop_event.is_set():
        remaining = end - time.monotonic()
        if remaining <= 0:
            return True
        time.sleep(min(remaining, 0.5))
    return False


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
        self.app = app
        self.playlist = app.config["Playlist"]

        self.stop_event = threading.Event()
        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

    def start(self):
        if not self.thread.is_alive():
            self.stop_event.clear()
            self.thread.start()
        else:
            print("BackgroundRefreshTask already running")

    def stop(self):
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()

    def _run(self):
        while not self.stop_event.is_set():
            active_id = self.playlist.get_active_plugin_id()
            next_id, schedule_delta = next_active_plugin(self.playlist, self.app)

            refresh_delta = None
            if active_id is not None:
                refresh_settings = self.playlist.get_plugin_refresh_timing(active_id)
                refresh_delta = json_to_timedelta(refresh_settings)

            events = []

            # Schedule refresh
            if active_id is not None and refresh_delta:
                events.append(("refresh", refresh_delta))

            # Schedule switch
            if next_id is not None and schedule_delta:
                events.append(("switch", schedule_delta))

            # Nothing to do
            if not events:
                sleep_interruptible(self.stop_event, 1)
                continue

            # Choose earliest event
            event, delta = min(events, key=lambda e: e[1])

            completed = sleep_interruptible(
                self.stop_event,
                delta.total_seconds(),
            )

            if not completed:
                break  # stop requested

            # Re-check stop after sleep
            if self.stop_event.is_set():
                break

            # Execute exactly one event
            if event == "switch":
                self.playlist.set_active_plugin_id(next_id)
                plugin = get_plugin_instance_by_id(next_id)
                plugin.render_image(self.app)


            elif event == "refresh":
                print(f"Refreshing plugin {active_id}")
                plugin = get_plugin_instance_by_id(active_id)
                plugin.render_image(self.app)


class TaskManager:
    def __init__(self):
        self.activeTasks: list[BaseTask] = []

    def submit_task(self, task: BaseTask):
        task.start()
