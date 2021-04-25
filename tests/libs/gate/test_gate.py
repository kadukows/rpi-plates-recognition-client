import rpiplatesrecignition_client
import time


def test_gate_initially_closed_and_not_opened(gate_controller):
    gate = gate_controller
    assert gate.is_closed() and not gate.is_opened()


def test_gate_open_will_make_gate_busy(gate_controller):
    gate = gate_controller
    gate.open()
    assert gate.is_busy()


def test_gate_state_change_will_leave_gate_not_in_valid_state(gate_controller):
    gate = gate_controller
    gate.open()
    assert not gate.is_closed() and not gate.is_opened()


def test_opening_gate_will_not_react_to_close_request(gate_controller):
    gate = gate_controller

    gate.open()

    time.sleep(0.5)
    gate.close()

    time.sleep(0.6)

    assert gate.is_opened() and not gate.is_closed()


def test_gate_opening_will_take_desired_time(gate_controller):

    gate = gate_controller

    gate.open()

    time.sleep(0.99)
    assert gate.is_busy()

    time.sleep(0.2)
    assert not gate.is_busy()


def test_gate_can_open_and_close(gate_controller):
    gate = gate_controller

    gate.open()
    time.sleep(1)
    assert gate.is_opened() and not gate.is_busy() and not gate.is_closed()

    gate.close()
    time.sleep(1)
    assert gate.is_closed() and not gate.is_busy() and not gate.is_opened()
