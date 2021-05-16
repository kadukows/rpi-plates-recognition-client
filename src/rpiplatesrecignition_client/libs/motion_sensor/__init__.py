from gpiozero import *

try:
    from .motion_sensor import RPIMotionSensor
    sensor = RPIMotionSensor()
except BadPinFactory as e:
    from .motion_sensor import MockMotionSensor
    sensor = MockMotionSensor()