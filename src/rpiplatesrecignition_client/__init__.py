import logging
import socketio
from .libs import logger_config
from .libs import example_module
from .libs.camera import camera
from .libs.gate import gate
from .libs.motion_sensor import sensor
import base64
import os
import pickle
import cv2 as cv2
import json
from threading import Lock



class CommandProxy:
    def __init__(self, sio, logger, unique_id):
        
        self.sio = sio
        self.photo_lock = Lock()
        self.logger = logger
        self.unique_id = unique_id
        sensor.notify_on_high_state(self.on_trigger_photo)
    
    def on_gate_request(self, command):
        config_string = self.sio.call(
            'update_config',
            data={'unique_id': self.unique_id},
            namespace='/rpi')

        json_config = json.loads(config_string)
        gate.update_config(json_config)
        command(self.sio)


    def on_trigger_photo(self):
        self.photo_lock.acquire()

        config_string = self.sio.call(
            'update_config',
            data={'unique_id': self.unique_id},
            namespace='/rpi')

        json_config = json.loads(config_string)

        camera.update_config(json_config)
        gate.update_config(json_config)

        img = camera.take_photo()


        logger.debug('Encoding image')
        image_string = base64.b64encode(
            cv2.imencode('.jpg', img)[1])

        logger.debug("Sending image to the server")
        sio.emit(
            'image_from_rpi',
            data=image_string,
            namespace='/rpi')
        logger.debug("Image sent")

        self.photo_lock.release()
    


def run(server, unique_id=''):
    assert server.startswith('http:')

    sio = socketio.Client()
    logger_config.logger_config(sio)
    logger = logging.getLogger('rpiplatesrecognition_client.init')
    proxy = None 

    @sio.event(namespace='/rpi')
    def connect():
        res = sio.call(
            'login_from_rpi',
            data={'unique_id': unique_id},
            namespace='/rpi')

        print('response to login call: ', res)
        proxy = CommandProxy(sio, logger, unique_id)
        sio.emit(
                'gate_controller_status',
                data={'status': "opened" if gate.is_open() else "closed"},
                namespace='/rpi')


    @sio.on('message_from_server_to_rpi', namespace='/rpi')
    def command(data):
        if isinstance(data, str):
            command_ = data

            if command_ == 'run_example_module':
                example_module.run()
            elif command_ == 'open_gate':
                logger.debug('open_gate was issued in command handler')
                proxy.on_gate_request(gate.open)
            elif command_ == 'close_gate':
                logger.debug('close_gate was issued in command handler')
                proxy.on_gate_request(gate.close)
            elif command_ == 'open_and_close_gate':
                logger.debug('open_and_close_gate was issued in command handler')
                proxy.on_gate_request(gate.open_and_close)
            elif command_ == 'trigger_photo':
                logger.debug("Take photo issued in command handler")
                proxy.on_trigger_photo()

            else:
                logger.warning(f'Unknown command: {command_}')

    
        

    sio.connect(server)
    sio.wait()
