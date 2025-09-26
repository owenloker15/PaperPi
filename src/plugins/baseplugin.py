import os

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

class BasePlugin():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.directory = os.path.join(PLUGIN_DIR, self.id)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_plugin_dir(self):
        return self.directory

    def get_settings_template(self):
        template_file = os.path.join(self.directory, "settings", "settings.html")
        if os.path.isfile(template_file) :
            return f"{self.get_id()}/settings/settings.html"

        return "BAAAD"

    def render_image(self, plugin_settings, app):
        pass
    
