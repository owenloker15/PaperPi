import importlib
import os

PLUGIN_INSTANCES = {}

def load_plugins(plugin_configs):
    for plugin_config in plugin_configs:
        plugin_id = plugin_config["id"]
        plugin_display_name = plugin_config["name"]
        module_name = f"plugins.{plugin_id}.{plugin_id}"
        class_name = plugin_config["class"]
        module = importlib.import_module(module_name)
        Plugin = getattr(module, class_name)
        plugin_instance = Plugin(plugin_id, plugin_display_name)
        PLUGIN_INSTANCES[plugin_id] = plugin_instance

def get_plugin_instance_by_config(plugin_config):
    id = plugin_config["id"]
    return PLUGIN_INSTANCES[id]

def get_plugin_instance_by_id(id):
    return PLUGIN_INSTANCES[id]