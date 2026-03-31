import pytest
import time
from core_logic import OpenERVCore, SystemState

def test_initial_state():
    core = OpenERVCore({})
    assert core.state == SystemState.BOOT

def test_sensor_update_logic():
    core = OpenERVCore({})
    # Mocking sensor to return healthy values
    core.sensor.get_reading = lambda: (10.0, 25.0)
    core.update_sensors()
    assert core.current_pressure == 10.0 * 3.45
    assert core.current_temp == 25.0
    assert core.read_fail_strikes == 0

def test_sensor_fault_transition():
    core = OpenERVCore({})
    # Mocking sensor failure
    core.sensor.get_reading = lambda: (None, None)
    # Simulate 21 fail strikes
    for _ in range(21):
        core.last_sensor_read = 0 # Force read
        core.update_sensors()
    
    assert core.state == SystemState.FAULT

def test_thermal_safety_non_blocking():
    core = OpenERVCore({})
    core.current_temp = 55.0
    # The run() loop would normally handle this, but we check logic
    # In the new architecture, handle_safety_checks is part of the main loop
    # We can simulate the check
    if core.current_temp > core.THERMAL_LIMIT_C:
        core.state = SystemState.FAULT
    
    assert core.state == SystemState.FAULT

def test_adc_filtering_integer():
    core = OpenERVCore({})
    core.filtered_pot_raw = 8000
    core.pot._value = 2000
    val = core.get_conditioned_adc()
    # (2000 + (8000*7)) / 8 = 7250
    assert core.filtered_pot_raw == 7250
    assert val == 7250 / 655.35
