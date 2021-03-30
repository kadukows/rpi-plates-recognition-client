import socketio
from rpiplatesrecignition_client.libs.gate import gate


def run(server, unique_id=''):
    sio = socketio.Client()

    @sio.event
    def connect():
        sio.emit('login', data={'unique-id': unique_id})

    @sio.on('open_gate')
    def open_gate():
        gate.open()
        #todo, return statues eg. if gate is open or not

    @sio.on('close_gate')
    def close_gate():
        gate.close()
        #todo, return statues eg. if gate is open or not

        

    sio.connect(server)
    sio.wait()
