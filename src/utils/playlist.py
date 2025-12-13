from flask import current_app


class Playlist:
    def __init__(self) -> None:
        self.active_plugin_id = None
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
        return {}

    def set_plugin_schedule(self, plugin_id, schedule_settings):
        self.plugin_schedule[plugin_id] = schedule_settings

    def get_plugin_schedule(self, plugin_id):
        if plugin_id in self.plugin_schedule:
            return self.plugin_schedule[plugin_id]
        print(f"No schedule found for {plugin_id}")
        return {}

    def get_all_plugin_schedules(self):
        app_config = current_app.config["Configuration"]
        plugin_configs = app_config.get_plugin_configs()
        schedules = []
        for plugin_config in plugin_configs:
            plugin_id = plugin_config.get("id")
            schedule_settings = self.get_plugin_schedule(plugin_id)
            schedule_settings["id"] = plugin_id
            schedules.append(schedule_settings)

    def get_playlist_settings_for_all(self):
        app_config = current_app.config["Configuration"]
        plugin_configs = app_config.get_plugin_configs()
        settings_data = []
        for plugin_config in plugin_configs:
            plugin_id = plugin_config.get("id")
            plugin_name = plugin_config.get("name")
            refresh_settings = self.get_plugin_refresh_timing(plugin_id)
            schedule_settings = self.get_plugin_schedule(plugin_id)
            data = {
                "pluginId": plugin_id,
                "pluginName": plugin_name,
                "refreshSettings": refresh_settings,
                "scheduleSettings": schedule_settings,
            }
            settings_data.append(data)
        return settings_data
