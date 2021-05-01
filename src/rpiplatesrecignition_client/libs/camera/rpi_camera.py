import cv2 as cv2
import subprocess
import secrets
from typing import Tuple
import hashlib
import logging
from dataclasses import dataclass
import json


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

    def take_photo(self):
        if(self.is_raspberrypi):
            self.logger.debug(
                'Camera module ran on RPI, preparing filename now')

            token = secrets.token_hex(32)
            full_filename = "/tmp/" + \
                str(int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16) % 10**8) + \
                ".jpg"

            cmd = "raspistill -n -o " + full_filename + \
                  " -w " + str(self.Config.img_size[0]) + \
                  " -h " + str(self.Config.img_size[1]) + \
                  " -t " + str(self.Config.timeout_in_ms) + \
                  " -sh " +str(self.Config.sharpness) + \
                  " -co " +str(self.Config.contrast) + \
                  " -br " +str(self.Config.brightness) + \
                  " -sa " +str(self.Config.saturation) + \
                  " -q " + str(self.Config.quality)
            
            
            self.logger.debug('Calling raspistill as: ' + cmd)
            subprocess.call(cmd, shell=True)

            self.logger.debug('Reading image with CV2')
            img = cv2.imread(full_filename)
        else:
            self.logger.warning('Camera module ran on NON-RPI device, sending sample image')       
            img = cv2.imread('plate.jpg')
            token = 'debug_image'

        return token, img
