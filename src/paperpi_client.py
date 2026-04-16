from socketio import Client

sio = Client()


@sio.on("connect")
def on_connect():
    print("Connected to server")


@sio.on("update")
def on_update(data):
    print("Got update:", data)


port = os.getenv("PORT")
sio.connect(f"http://localhost:{port}")
sio.wait()
