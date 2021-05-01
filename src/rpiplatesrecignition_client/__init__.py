import logging
import socketio
from .libs import logger_config
from .libs import example_module
from .libs.camera import camera
from .libs.gate import gate
import base64
import os
import pickle
import cv2 as cv2
import json





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
                logger.debug('open_gate was issued in command handler')
                gate.open()
            elif command_ == 'close_gate':
                logger.debug('close_gate was issued in command handler')
                gate.close()

            elif command_ == 'trigger_photo':
                
                logger.debug("Take photo issued in command handler")
                on_trigger_photo()

            else:
                logger.warning(f'Unknown command: {command_}')
                
    def on_trigger_photo():
        config_string = sio.call(
            'update_config',
            data={'unique_id': unique_id},
            namespace='/rpi')

        json_config = json.loads(config_string)

        camera.update_config(json_config)

        _, img = camera.take_photo()

        logger.debug('Encoding image')
        image_string = base64.b64encode(
            cv2.imencode('.jpg', img)[1])

        logger.debug("Sending image to the server")
        res = sio.call(
            'image_from_rpi',
            data=image_string,
            namespace='/rpi')

    sio.connect(server)
    sio.wait()
