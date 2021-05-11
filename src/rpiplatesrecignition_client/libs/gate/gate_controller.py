from gpiozero import OutputDevice
import datetime
from time import sleep
import logging
from dataclasses import dataclass
import json
from threading import Thread
from threading import Lock


class GateController:
    @dataclass
    class Config:
        gpio_pin_number: int = 3
        button_press_time: float = 0.35 
        gate_opening_time: float = 15
        time_to_drive_in: float = 5
        

    def __init__(self):
        self.current_gpio_pin_number = self.Config.gpio_pin_number
        self.lock = Lock()
        self.is_opened = False

        self.logger = logging.getLogger('rpiplatesrecognition_client.GateController')
        
    def update_config(self, config: json):
        self.Config.gpio_pin_number = config['gatecontroller_gpio_pin_number']
        self.Config.button_press_time = config['gatecontroller_button_press_time']
        self.Config.gate_opening_time = config['gatecontroller_gate_opening_time']
        self.Config.time_to_drive_in = config['gatecontroller_time_to_drive_in']

        if not self.current_gpio_pin_number == self.Config.gpio_pin_number:
            try:
                self.gpio_pin.close()
                self.gpio_pin = OutputDevice(self.Config.gpio_pin_number)
                self.gpio_pin.off()
                self.current_gpio_pin_number = self.Config.gpio_pin_number
            except Exception:
                self.logger.warning("Unable to change output gpio pin (pin probably in use)!")

    def __wait_and_close(self):
        sleep(self.Config.time_to_drive_in)
        self.close()

    def is_open(self):
        return self.is_opened()

    def is_busy(self):
        return self.lock.locked()

    # it is safe to call each of the following without checking for is_busy or is_opened/closed response
    # the gate is not supposed to stop or moving opposite direction
    def open_and_close(self):
        self.logger.debug("[OPEN and CLOSE] beggining procedure")
        self.open()
        thread = Thread(target = self.__wait_and_close)
        thread.start()

    def open(self):
        self.logger.debug("[OPEN] In open function - checking if gate not open")
        if not self.is_opened:
            self.lock.acquire()
            self.logger.debug("[OPEN] Gate not open - lock acquired, pressing button for " + 
                        str(self.Config.button_press_time) + "s" + 
                        "and waiting for gate to be opened for: " + str(self.Config.gate_opening_time))
            self.press_button()
            sleep(self.Config.gate_opening_time)
            self.is_opened = True
            self.logger.debug("[OPEN] Gate opened, releasing lock")
            self.lock.release()

    def close(self):
       self.logger.debug("[CLOSE] In close function - checking if gate open")
       if self.is_opened:
            self.logger.debug("[CLOSE] Gate open - lock acquired, pressing button for " + 
                        str(self.Config.button_press_time) + "s" + 
                        "and waiting for gate to be closed for: " + str(self.Config.gate_opening_time))
            self.lock.acquire()
            self.press_button()
            sleep(self.Config.gate_opening_time)
            self.is_opened = False
            self.logger.debug("[CLOSE] Gate closed, releasing lock")
            self.lock.release()

           
class RPIGateController(GateController):        
    def __init__(self):
        super().__init__()
        self.gpio_pin = OutputDevice(self.Config.gpio_pin_number)
        self.gpio_pin.off()
        self.logger = logging.getLogger('rpiplatesrecognition_client.RPIGateController')
        

    def press_button(self):
        self.logger.debug("Pressing button for: " + str(self.Config.button_press_time) + "seconds")
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

    