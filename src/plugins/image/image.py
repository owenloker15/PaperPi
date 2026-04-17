import random

from PIL import Image

from plugins.baseplugin import BasePlugin
from utils.render_utils import send_image


class ImagePlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)

    def render_image(self, app):
        plugin_settings = self.get_settings()
        images = plugin_settings.get("images", [])

        if not images:
            print("No images found!")
            return

        # Pick a random image
        image_path = random.choice(images)

        # Open the image with PIL
        image = Image.open(image_path).convert("RGBA")

        # Update the display with the PIL image
        send_image(image)
