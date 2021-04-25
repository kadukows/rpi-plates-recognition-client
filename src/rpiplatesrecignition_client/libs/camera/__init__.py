from .rpi_camera import RaspberryPiCamera


def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False


camera = RaspberryPiCamera(is_raspberrypi())