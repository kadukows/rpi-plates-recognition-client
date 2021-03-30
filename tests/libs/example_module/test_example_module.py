import rpiplatesrecignition_client
from rpiplatesrecignition_client.libs.example_module import run

def test_example_module(client_server_with_gathered_logs):
    client, server, logs = client_server_with_gathered_logs

    rpiplatesrecignition_client.run('', '')

    server.emit('run_example_module')
    assert 'example module was ran' in logs.messages_from('rpiplatesrecognition_client.example_module')
