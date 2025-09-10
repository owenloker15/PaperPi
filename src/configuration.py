import json
import os
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")


class Configuration:
    def __init__(self):
        self.plugin_configs = self.load_plugin_configs()

    def load_plugin_configs(self):
        plugins_list = []
        for plugin_dir_name in sorted(os.listdir(PLUGINS_DIR)):
            plugin_dir = os.path.join(PLUGINS_DIR, plugin_dir_name)
            if os.path.isdir(plugin_dir) and plugin_dir != os.path.join(PLUGINS_DIR, "__pycache__"):
                plugin_config_file_path = os.path.join(plugin_dir, "plugin-config.json")
                if os.path.isfile(plugin_config_file_path):
                    with open(plugin_config_file_path, "r") as file:
                        plugin_info = json.load(file)
                        plugins_list.append(plugin_info)

        return plugins_list

    def get_plugin_configs(self):
        return self.plugin_configs
    
    def get_plugin_config(self, plugin_id):
        return next((plugin for plugin in self.plugin_configs if plugin['id'] == plugin_id), None)
