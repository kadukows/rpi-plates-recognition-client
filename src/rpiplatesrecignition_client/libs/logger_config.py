import logging, logging.handlers


def logger_config(sio, with_file=False):
    """Method with logger configuration"""

    logger = logging.getLogger('rpiplatesrecognition_client')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    class SocketioHandler(logging.NullHandler):
        def __init__(self, sio):
            logging.Handler.__init__(self)
            self.sio = sio

        def handle(self, record):
            self.sio.emit('log_from_rpi', formatter.format(record), namespace='/rpi')

    sh = SocketioHandler(sio)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if with_file:
        fh = logging.FileHandler('rpiplatesrecognition_client.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
