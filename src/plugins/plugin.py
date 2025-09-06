import os

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

class Plugin():
    def __init__(self, name) -> None:
        self.name = name
        self.directory = os.path.join(PLUGIN_DIR, self.name.lower())

    def get_name(self):
        return self.name

    def get_plugin_dir(self):
        return self.directory

    def get_template(self):
        template_file = os.path.join(self.directory, "settings.html")
        print(template_file)
        if os.path.isfile(template_file) :
            return template_file
        return "BAAAD"
