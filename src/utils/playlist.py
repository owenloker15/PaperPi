from datetime import time, timedelta


class Playlist:
    def __init__(self) -> None:
        self.active_plugin_id = ""
        # When to set a plugin as the active plugin
        self.plugin_schedule = {}
        # How often to refresh a plugin's display if it is active
        self.refresh_settings = {}

    def set_active_plugin_id(self, plugin_id):
        self.active_plugin_id = plugin_id

    def get_active_plugin_id(self):
        return self.active_plugin_id

    def set_plugin_refresh_timing(self, plugin_id, refresh_settings):
        self.refresh_settings[plugin_id] = refresh_settings

    def get_plugin_refresh_timing(self, plugin_id):
        if plugin_id in self.refresh_settings:
            return self.refresh_settings[plugin_id]
        print(f"No refresh settings found for {plugin_id}")

    def set_plugin_schedule(self, plugin_id, time_of_day: time):
        self.plugin_schedule[plugin_id] = time_of_day

    def get_plugin_schedule(self, plugin_id):
        if plugin_id in self.plugin_schedule:
            return self.plugin_schedule[plugin_id]
        print(f"No schedule found for {plugin_id}")
