import cv2 as cv2
import subprocess
import secrets
from typing import Tuple
import hashlib
import logging


class RaspberryPiCamera():
    def __init__(self, is_raspberrypi):
        self.is_raspberrypi = is_raspberrypi
        self.logger = logging.getLogger('rpiplatesrecognition_client.RaspberryPiCamera')


    def take_photo(self):
        if(self.is_raspberrypi):     
            self.logger.debug('Camera module ran on RPI, preparing filename now')

            token = secrets.token_hex(32)
            full_filename = "/tmp/" + \
                        str(int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16) %10**8) + \
                        ".jpg"

            cmd = "raspistill -w 1280 -h 960 -t 2000 -n -o " + full_filename
            subprocess.call(cmd, shell=True)
            self.logger.debug('Calling raspistill in subprocess')

            self.logger.debug('Reading image with CV2')
            img = cv2.imread(full_filename)
        else:
            self.logger.warning('Camera module ran on NON-RPI device')
            img = cv2.imread('plate.jpg')
            token = 'debug_image'
        
        return token, img