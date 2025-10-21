from display.idisplay import IDisplay
from pathlib import Path
import os
import json

from display.inky_display import InkyDisplay
from display.mock_display import MockDisplay

class DisplayManager:
    def __init__(self):
        self.display = None

        device_config_file = Path(os.getenv("PROJECT_SRC"), "config", "device_config.json")
        with open(device_config_file, "r") as file:
            data = json.load(file)
        
        res_width = data['resolution']['width']
        res_heght = data['resolution']['height']
        self.set_resolution(res_width, res_heght)

        display_type = data['type']
        match display_type:
            case "mock":
                self.set_display(MockDisplay(data))
            case "inky":
                self.set_display(InkyDisplay(data))
            case _:
                print(f"{display_type} display not found!")

    def set_resolution(self, width, height):
        self.resolution = (width, height)

    def get_resolution(self):
        return self.resolution

    def set_display(self, display: IDisplay):
        self.display = display
    
    def get_display(self):
        return self.display

    def update_display(self, img):
        if img is None:
            print("Image was empty!")
            return

        if self.display is None:
            print("Display is empty!")
            return
        
        self.display.upload_image(img)