import os

plugin_dir = os.path.dirname(os.path.abspath(__file__))

class Plugin():
    def __init__(self, name) -> None:
        self.name = name
        self.directory = os.path.join(plugin_dir, self.name)

    def get_name(self):
        return self.name

    def get_plugin_dir(self):
        return self.directory

    def get_template(self):
        return self.get_name
