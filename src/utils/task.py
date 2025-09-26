import threading
import time

from utils.plugin_utils import get_plugin_instance_by_id

class BaseTask():
    def _run():
        pass

    def start():
        pass

    def stop():
        pass

    def onComplete(self, callback = None):
        if callback is not None:
            callback()

class ManualRefreshTask(BaseTask):
    def __init__(self, plugin_id, plugin_settings, app):
        self.plugin_id = plugin_id
        self.plugin_settings = plugin_settings

        self.thread = threading.Thread(target = self._run, args=(app,), daemon=True)

    def start(self):
        self.thread.start()

    def _run(self, app):
        plugin_instance = get_plugin_instance_by_id(self.plugin_id)
        return plugin_instance.render_image(self.plugin_settings, app)


class BackgroundRefreshTask(BaseTask):
    def __init__(self, plugin_id, plugin_settings):
        self.plugin_id = plugin_id
        self.plugin_settings = plugin_settings
        self.thread = None
        self.running = False

    def start(self):
        if not self.running:
            self.thread = threading.Thread(target=self._run, daemon=True)
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


    def _run(self):
        while self.running:
            print("hi!")
            time.sleep(10)

class TaskManager():
    def __init__(self):
        self.activeTasks = list[BaseTask]

    def submit_task(self, task: BaseTask):
        task.start()
