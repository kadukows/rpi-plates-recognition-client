from gpiozero import OutputDevice
import datetime
from time import sleep
import logging
from dataclasses import dataclass
import json

class GateController:
    @dataclass
    class Config:
        gpio_pin_number: int = 3
        button_press_time: float = 0.35 
        gate_opening_time: float = 15
        

    def __init__(self):
        self.init_state_change_time = datetime.datetime.now() - datetime.timedelta(seconds=self.Config.gate_opening_time)
        
        self.opened = False
        self.is_closing = False
        self.is_opening = False
        self.logger = logging.getLogger('rpiplatesrecognition_client.GateController')
        
    def update_config(self, config: json):
        self.Config.gpio_pin_number = config['gatecontroller_gpio_pin_number']
        self.Config.button_press_time = config['gatecontroller_button_press_time']
        self.Config.gate_opening_time = config['gatecontroller_gate_opening_time']

        try:
            self.gpio_pin = OutputDevice(self.Config.gpio_pin_number)
            self.gpio_pin.off()
        except Exception:
            self.logger.warning("Unable to change output gpio pin!")

    # check for busy state and update open/close state of the gate
    def is_busy(self) -> bool:
        if(datetime.datetime.now() < self.init_state_change_time + datetime.timedelta(seconds=self.Config.gate_opening_time)):
            return True
        else:
            if self.is_closing and not self.is_opening:
                self.opened = False
                self.is_closing = False

            elif self.is_opening and not self.is_closing:
                self.opened = True
                self.is_opening = False

            return False

    def is_opened(self):
        if not self.is_busy():
            return self.opened
        return False

    def is_closed(self):
        if not self.is_busy():
            return not self.opened
        return False

    # it is safe to call each of the following without checking for is_busy or is_opened/closed response
    # the gate is not supposed to stop or moving opposite direction
    def open(self):
        self.logger.debug("Request to open gate for: " + str(self.Config.gate_opening_time) + "seconds")
        if not self.is_busy():
            self.logger.debug("[OPEN] Gate not busy")
            if not self.opened:
                self.logger.debug("[OPEN] Gate not open")
                
                self.press_button()
                self.is_opening = True
                self.init_state_change_time = datetime.datetime.now()

    def close(self):
        self.logger.debug("Request to open gate for: " + str(self.Config.gate_opening_time) + "seconds")
        if not self.is_busy():
            self.logger.debug("[CLOSE] Gate not busy")
            if self.opened:
                self.logger.debug("[CLOSE] Gate not open")
                self.press_button()
                self.opened = False
                self.is_closing = True
                self.init_state_change_time = datetime.datetime.now()



class RPIGateController(GateController):        
    def __init__(self):
        super().__init__()
        self.gpio_pin = OutputDevice(self.Config.gpio_pin_number)
        self.gpio_pin.off()
        self.logger = logging.getLogger('rpiplatesrecognition_client.RPIGateController')
        

    def press_button(self):
        self.logger.debug("Pressing button for: " + str(self.button_press_time) + "seconds")
        self.gpio_pin.on()
        sleep(self.Config.button_press_time)
        self.gpio_pin.off()



class MockGateController(GateController):        
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('rpiplatesrecognition_client.MockGateController')
        

    def press_button(self):
        self.logger.debug("Mock Pressing button for: " + str(self.Config.button_press_time) + "seconds")
        sleep(self.Config.button_press_time)        

    