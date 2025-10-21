from display.idisplay import IDisplay

class MockDisplay(IDisplay):
    def __init__(self, device_config):
        super().__init__(device_config)

    def upload_image(self, img):
        img.show()