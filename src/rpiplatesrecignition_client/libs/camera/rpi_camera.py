import cv2 as cv2
import subprocess
import secrets
from typing import Tuple
import hashlib
import logging
from dataclasses import dataclass
from io import BytesIO
import numpy as np
import base64
import os
import cv2 as cv2
import json
import socketio
import picamera
import io
import time
import base64

class RaspberryPiCamera():
    @dataclass
    class Config:
        img_size: Tuple[int, int] = (800, 600)
        timeout_in_ms: int = 2000 #do not go below 1200
        sharpness: int = 0 #-100 - 100
        contrast: int = 0 #-100 - 100
        brightness: int = 0 #-100 - 100
        saturation: int = 0 #-100 - 100
        quality: int = 100 #0 - 100

    def __init__(self, is_raspberrypi):
        self.is_raspberrypi = is_raspberrypi
        self.logger = logging.getLogger(
            'rpiplatesrecognition_client.RaspberryPiCamera')

    def update_config(self, config: json):
        self.Config.img_size = config['img_size']
        self.Config.timeout_in_ms = config['camera_timeout_in_ms']
        self.Config.sharpness = config['camera_sharpness']
        self.Config.contrast = config['camera_contrast']
        self.Config.brightness = config['camera_brightness']
        self.Config.saturation = config['camera_saturation']
        self.Config.quality = config['camera_quality']

    def check_motion(self,frame, past_frame, min_area):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 5) 

        if past_frame is None:
            past_frame = gray
            return past_frame

        frame_detla = cv2.absdiff(past_frame, gray)

        thresh = cv2.threshold(frame_detla, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        if cnts is not None:
            for c in cnts:
                if cv2.contourArea(c) < min_area:
                    continue
                else:
                    self.logger.debug("Motion detected!")
                    self.send_frame(frame)
                    return
    
    def send_frame(self, frame):
        self.logger.debug('Encoding image')
        image_string = base64.b64encode(cv2.imencode('.jpg', frame)[1])

        self.logger.debug("Sending frame to the server")
        self.sio.emit(
            'image_from_rpi',
            data=image_string,
            namespace='/rpi')
        self.logger.debug("Frame sent")
        time.sleep(2)

    def start_streaming(self,sio):
        self.sio = sio
        min_area = 250
        past_frame = None
        self.logger.debug('Camera module ran on RPI, preparing streaming and motion detection')
        
        camera = picamera.PiCamera()
        camera.resolution = self.Config.img_size
        #camera.brightness = self.Config.brightness
        #camera.sharpness = self.Config.sharpness
        #camera.contrast = self.Config.contrast
        #camera.saturation = self.Config.saturation

        self.logger.debug('Streamming started')

        while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=False)
            data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            frame = cv2.imdecode(data, 1)
            if frame is not None:
                past_frame = self.check_motion(frame, past_frame, min_area)
            else:
                self.logger.debug('Streamming error')

            time.sleep(0.5)
            
    def take_photo(self):
        self.logger.debug(
                'Taking photo is depreciated.')

        if(self.is_raspberrypi):
            self.logger.debug(
                'Camera module ran on RPI, preparing raspistill command now')

            cmd = "raspistill -n -o -" + \
                  " -w " + str(self.Config.img_size[0]) + \
                  " -h " + str(self.Config.img_size[1]) + \
                  " -t " + str(self.Config.timeout_in_ms) + \
                  " -sh " +str(self.Config.sharpness) + \
                  " -co " +str(self.Config.contrast) + \
                  " -br " +str(self.Config.brightness) + \
                  " -sa " +str(self.Config.saturation) + \
                  " -q " + str(self.Config.quality)

            self.logger.debug('Raspistill command : ' + cmd)

            img_stream = BytesIO()
            self.logger.debug('Writing output to buffer and creating img_array')
            img_stream.write(subprocess.check_output(cmd, shell=True))
            img_stream.seek(0)
            img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)


            self.logger.debug('Decoding image with CV2')
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        else:
            self.logger.warning('Camera module ran on NON-RPI device, sending sample image')
            img = cv2.imread('debug.jpg')

        return img
