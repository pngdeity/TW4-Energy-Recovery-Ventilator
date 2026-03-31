import pytest
from core_logic import OpenERVCore

def test_thermal_safety():
    core = OpenERVCore({})
    core.current_temp = 25.0
    assert core.handle_safety_checks() is True
    assert core.thermal_shutdown_active is False
    
    # Trigger shutdown
    core.current_temp = 55.0
    assert core.handle_safety_checks() is False
    assert core.thermal_shutdown_active is True
    # Fans should be 0
    assert core.fans.fans['i0'].pwm._duty == 0

def test_adc_filtering():
    core = OpenERVCore({})
    # Mocking ADC read
    core.pot._value = 10000
    val1 = core.get_conditioned_adc()
    
    core.pot._value = 20000
    val2 = core.get_conditioned_adc()
    
    # EMA should smooth the transition
    assert val2 > val1
    assert val2 < (20000 / 655.35) # Should not have reached target immediately
