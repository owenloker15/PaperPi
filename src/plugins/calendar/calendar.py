from plugins.baseplugin import BasePlugin

class CalendarPlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)

    def render_image(self, plugin_settings):
        return take_screenshot_html()