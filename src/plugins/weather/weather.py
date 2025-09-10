from plugins.baseplugin import BasePlugin

class WeatherPlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)