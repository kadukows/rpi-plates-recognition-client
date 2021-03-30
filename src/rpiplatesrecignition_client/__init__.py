import logging, socketio
from .libs import logger_config
from .libs import example_module

def run(server, unique_id=''):
    sio = socketio.Client()
    logger_config.logger_config(sio)
    logger = logging.getLogger('rpiplatesrecognition_client.init')

    @sio.event
    def connect():
        sio.emit('login', data={'unique-id': unique_id})

    @sio.on('open_gate')
    def open_gate():
        # open gate
        logger.debug('received open gate message')
        pass

    @sio.on('run_example_module')
    def run_example_module():
        example_module.run()

    sio.connect(server)
    sio.wait()
