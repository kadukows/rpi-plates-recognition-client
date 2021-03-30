import socketio
from rpiplatesrecignition_client.libs.camera import camera


def run(server, unique_id=''):
    sio = socketio.Client()

    @sio.event
    def connect():
        sio.emit('login', data={'unique-id': unique_id})

    @sio.on('open_gate')
    def open_gate():
        # open gate
        pass

    @sio.on('take_photo')
    def take_photo():
        [token, img] = camera.take_photo()
        

    sio.connect(server)
    sio.wait()
