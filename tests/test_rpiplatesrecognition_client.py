import rpiplatesrecignition_client
from rpiplatesrecignition_client.libs.gate import gate

def test_rpiplatesrecognition_client_will_call_login_upon_connecting(client_server):
    client, server = client_server
    unique_id = 'some_unique_id_on_rpi'

    class Recorder:
        called = False

    @server.on('login')
    def login(data):
        Recorder.called = True
        assert 'unique-id' in data and data['unique-id'] == unique_id

    rpiplatesrecignition_client.run('', unique_id)
    assert Recorder.called

def test_gate_open_will_make_gate_busy(client_server):
    assert gate.is_closed()
    
    client, server = client_server
    unique_id = 'some_unique_id_on_rpi'
    rpiplatesrecignition_client.run('', unique_id)
    server.emit("open_gate")

    assert gate.is_busy()
