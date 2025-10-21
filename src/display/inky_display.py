from display.idisplay import IDisplay

class InkyDisplay(IDisplay):
    def __init__(self, device_config):
        super().__init__(device_config)
        self.inky = None
        print("Created inky display")
        try:
            from inky.auto import auto
            self.inky = auto()
            print("Inky found!")
        except (ImportError, RuntimeError):
            print("Inky not found!")

    def upload_image(self, img):
        if self.inky is None:
            print("Inky was not found!")
            return

        resoulution = self.device_config['resolution']
        img = img.convert("RGB").resize((resoulution['width'], resoulution['height']))
        img.load()

        self.inky.set_image(img)
        print("Uploading image!")
        self.inky.show()
        print("Image uploaded!")