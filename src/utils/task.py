import threading
import time

class ManualRefreshTask():
    def __init__(self, plugin_id, plugin_settings):
        self.plugin_id = plugin_id
        self.plugin_settings = plugin_settings

        self.thread = threading.Thread(target = self._run, daemon=True)
        self.thread.start()

    def _run(self):
        time.sleep(5)
        print("HIIIIII")


class BackgroundRefreshTask():
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

