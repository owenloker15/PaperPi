import threading

from display.idisplay import IDisplay

mutex = threading.Lock()


class MockDisplay(IDisplay):
    def __init__(self, device_config):
        super().__init__(device_config)

    def upload_image(self, img):
        with mutex:
            print("Showing image!")
            img.show()
            print("Image shown!")

