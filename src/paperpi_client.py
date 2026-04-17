import base64
import os

from dotenv import load_dotenv
from socketio import Client
from PIL import Image
from io import BytesIO

from display.display_manager import DisplayManager

sio = Client()
display_manager = DisplayManager()

load_dotenv()

@sio.on("connect")
def on_connect():
    print("Connected to server")

@sio.on("update_display")
def on_update_display(data):
    img_bytes = base64.b64decode(data["data"])
    img = Image.open(BytesIO(img_bytes))

    display_manager.update_display(img)

    print("Display updated")

# Read host and port from environment (with sensible defaults)
host = os.getenv("SERVER_HOST", "192.168.1.93")  # <-- change this default
port = os.getenv("PORT", "5000")

url = f"http://{host}:{port}"

print(f"Connecting to {url}...")
sio.connect(url)

sio.wait()