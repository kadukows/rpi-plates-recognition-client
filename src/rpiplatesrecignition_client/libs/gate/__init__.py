from gpiozero import *

try:
    from .gate_controller import RPIGateController
    gate = RPIGateController()
except BadPinFactory as e:
    from .gate_controller import MockGateController
    gate = MockGateController()