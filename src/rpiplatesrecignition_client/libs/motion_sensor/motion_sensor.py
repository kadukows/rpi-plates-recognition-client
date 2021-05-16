from gpiozero import DigitalInputDevice
import datetime
from time import sleep
import logging
from dataclasses import dataclass
import json
from threading import Thread
from threading import Lock


class MotionSensor:
    @dataclass
    class Config:
        gpio_pin_number: int = 4

    def __init__(self):
        self.logger = logging.getLogger('rpiplatesrecognition_client.MotionSensor')
        self.current_gpio_pin_number = self.Config.gpio_pin_number
        self.input_device = DigitalInputDevice(self.current_gpio_pin_number, pull_up=False, bounce_time=1)

    def update_config(self, config: json):
        self.Config.gpio_pin_number = config['motionsensor_gpio_pin_number']

        if not self.current_gpio_pin_number == self.Config.gpio_pin_number:
            try:
                self.gpio_pin.close()
                self.input_device = DigitalInputDevice(self.current_gpio_pin_number, pull_up=False, bounce_time=1)

                self.gpio_pin.off()
                self.current_gpio_pin_number = self.Config.gpio_pin_number
            except Exception:
                self.logger.warning("Unable to change output gpio pin (pin probably in use)!")

    def __wait_for_high_state(self, function):
        self.input_device.wait_for_active()
        function()

    def notify_on_high_state(self, function):
        thread = Thread(target = self.__wait_for_high_state, args=[function])
        thread.start()
        