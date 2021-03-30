import rpiplatesrecignition_client
import datetime


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

def test_rpiplatesrecognition_client_will_log_open_gate_message(client_server_with_gathered_logs):
    client, server, logs = client_server_with_gathered_logs

    rpiplatesrecignition_client.run('', '')
    server.emit('open_gate')

    assert 'received open gate message' in logs.messages_from('rpiplatesrecognition_client.init')
