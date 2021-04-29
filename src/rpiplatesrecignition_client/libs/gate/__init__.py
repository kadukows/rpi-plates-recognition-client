from gpiozero import *


try:
    from .gate_controller import GateController
    gate = GateController(
        gpio_pin=3, button_press_time_s=0.350, gate_opening_time_s=15)
except BadPinFactory as e:
    from .mock_gate_controller import MockGateController
    gate = MockGateController(
        gpio_pin=3, button_press_time_s=0.350, gate_opening_time_s=15)