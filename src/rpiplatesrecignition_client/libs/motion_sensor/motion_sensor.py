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
        self.current_gpio_pin_number = self.Config.gpio_pin_number

    def update_config(self, config: json):
        self.Config.gpio_pin_number = config['motionsensor_gpio_pin_number']

        if not self.current_gpio_pin_number == self.Config.gpio_pin_number:
            try:
                self.gpio_pin.close()
                self.input_device = DigitalInputDevice(self.current_gpio_pin_number, pull_up=False, bounce_time=1)

                self.gpio_pin.off()
                self.current_gpio_pin_number = self.Config.gpio_pin_number
            except Exception:
                self.logger.warning("Unable to change input gpio pin (pin probably in use) or!")

    def notify_on_high_state(self, function):
        self.logger.debug("Starting thread to wait for high state")
        thread = Thread(target = self.wait_for_high_state, args=[function])
        thread.start()
        

class RPIMotionSensor(MotionSensor):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('rpiplatesrecognition_client.RPIMotionSensor')
        self.input_device = DigitalInputDevice(self.current_gpio_pin_number, pull_up=False, bounce_time=1)

    def wait_for_high_state(self, function):
        self.input_device.wait_for_active()
        self.logger.debug("Motion detected, invoking trigger photo")
        function()


class MockMotionSensor(MotionSensor):
    def __init__(self):
        self.logger = logging.getLogger('rpiplatesrecognition_client.RPIMotionSensor')
        self.logger.debug("[MOCK_MOTION] Just a mock class")
        super().__init__()

    def wait_for_high_state(self, function):
        self.logger.debug("[MOCK_MOTION] Waiting for high state (forever)")
