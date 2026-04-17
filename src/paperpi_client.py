import os
from socketio import Client

sio = Client()


@sio.on("connect")
def on_connect():
    print("Connected to server")


@sio.on("update")
def on_update(data):
    print("Got update:", data)


# Read host and port from environment (with sensible defaults)
host = os.getenv("SERVER_HOST", "172.18.32.1")  # <-- change this default
port = os.getenv("PORT", "5000")

url = f"http://{host}:{port}"

print(f"Connecting to {url}...")
sio.connect(url)

sio.wait()