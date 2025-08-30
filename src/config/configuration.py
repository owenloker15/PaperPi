from flask import current_app

def get_configuration_helper():
    return current_app.config["Configuration"]

class Configuration():
    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def get_plugins(self):
        return self.plugins

    def get_plugin_by_name(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return {}

