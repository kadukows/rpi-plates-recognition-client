import socketio

def run(server, unique_id=''):
    sio = socketio.Client()

    @sio.event
    def connect():
        sio.emit('login', data={'unique-id': unique_id})

    @sio.on('open_gate')
    def open_gate():
        # open gate
        pass

    sio.connect(server)
    sio.wait()
