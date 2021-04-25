import logging, socketio
from .libs import logger_config
from .libs import example_module

def run(server, unique_id=''):
    assert server.startswith('http:')

    sio = socketio.Client()
    logger_config.logger_config(sio)
    logger = logging.getLogger('rpiplatesrecognition_client.init')

    @sio.event(namespace='/rpi')
    def connect():
        res = sio.call(
            'login_from_rpi',
            data={'unique_id': unique_id},
            namespace='/rpi')

        print('response to login call: ', res)

    @sio.on('message_from_server_to_rpi', namespace='/rpi')
    def command(data):
        if isinstance(data, str):
            command_ = data

            if command_ == 'run_example_module':
                example_module.run()
            elif command_ == 'open_gate':
                logger.debug('open_gate was issued')
            else:
                logger.warning(f'Unknown command: {command_}')

    sio.connect(server)
    sio.wait()