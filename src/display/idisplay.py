class IDisplay:
    def __init__(self, device_config):
        self.device_config = device_config
    
    def upload_image(self, img):
        raise NotImplementedError("Upload image must be implemented by a derived class!")