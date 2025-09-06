from plugins.plugin import Plugin

class WeatherPlugin(Plugin):
    def __init__(self, id, name):
        super().__init__(id, name)