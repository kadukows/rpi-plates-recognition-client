from gpiozero import OutputDevice
import datetime
from time import sleep
import logging


class GateController:
    def __init__(self, gpio_pin, button_press_time_s, gate_opening_time_s):
        self.gpio_pin = gpio_pin
        self.button_press_time = button_press_time_s
        self.gate_opening_time = gate_opening_time_s
        self.init_state_change_time = datetime.datetime.now(
        ) - datetime.timedelta(seconds=self.gate_opening_time)
        self.gpio_pin = OutputDevice(gpio_pin)
        self.gpio_pin.off()
        self.opened = False
        self.is_closing = False
        self.is_opening = False
        self.logger = logging.getLogger('rpiplatesrecognition_client.GateController')
        

    def __press_button(self):
        self.logger.debug("Pressing button for: " + str(self.button_press_time) + "seconds")
        self.gpio_pin.on()
        sleep(self.button_press_time)
        self.gpio_pin.off()

    # check for busy state and update open/close state of the gate
    def is_busy(self) -> bool:
        if(datetime.datetime.now() < self.init_state_change_time + datetime.timedelta(seconds=self.gate_opening_time)):
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
        self.logger.debug("Beginning opening gate for: " + str(self.gate_opening_time) + "seconds")
        if not self.is_busy():
            self.logger.debug("[OPEN] Gate not busy")
            if not self.opened:
                self.logger.debug("[OPEN] Gate not open")
                
                self.__press_button()
                self.is_opening = True
                self.init_state_change_time = datetime.datetime.now()

    def close(self):
        self.logger.debug("Beginning closing gate for: " + str(self.gate_opening_time) + "seconds")
        if not self.is_busy():
            self.logger.debug("[CLOSE] Gate not busy")
            if self.opened:
                self.logger.debug("[CLOSE] Gate not open")
                self.__press_button()
                self.opened = False
                self.is_closing = True
                self.init_state_change_time = datetime.datetime.now()