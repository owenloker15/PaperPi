from flask import render_template
from plugins.baseplugin import BasePlugin
from utils.render_utils import screenshot_html

class CalendarPlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)

    def render_image(self, plugin_settings, app):
        with app.app_context():
            str = render_template("calendar/display/display.html", settings=plugin_settings)
            screenshot_html(str)
