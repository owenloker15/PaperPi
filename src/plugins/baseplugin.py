import os

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))


class BasePlugin:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.directory = os.path.join(PLUGIN_DIR, self.id)
        self.settings = {}

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_plugin_dir(self):
        return self.directory

    def get_settings_template(self):
        template_file = os.path.join(self.directory, "settings", "settings.html")
        if os.path.isfile(template_file):
            return f"{self.get_id()}/settings/settings.html"

        return f"Failed to find settings.html file for {self.name}"

    def save_settings(self, plugin_settings):
        self.settings = plugin_settings

    def get_settings(self):
        return self.settings

    def render_image(self, app):
        pass
