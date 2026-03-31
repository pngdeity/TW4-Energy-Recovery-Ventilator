import pytest
from fan_manager import FanManager, Fan

def test_fan_threshold():
    fan = Fan(0)
    # Test below threshold (17%)
    assert fan.set_speed(5) == 0
    assert fan.set_speed(16.9) == 0
    # Test above threshold
    assert fan.set_speed(20) == 20
    # Test clamping
    assert fan.set_speed(110) == 100
    assert fan.set_speed(-10) == 0

def test_fan_manager_init():
    fm = FanManager()
    assert len(fm.fans) == 4
    assert fm.fans['i0'].pwm._freq == 70000
    assert fm.fans['i1'].pwm._freq == 20000

def test_speed_to_action():
    fm = FanManager()
    # Positive speed (Ingress)
    r1, r2 = fm.speed_to_action(50, 0)
    assert fm.fans['i0'].pwm._duty > 0
    assert fm.fans['e0'].pwm._duty == 0
    
    # Negative speed (Egress)
    r1, r2 = fm.speed_to_action(-50, 0)
    assert fm.fans['i0'].pwm._duty == 0
    assert fm.fans['e0'].pwm._duty > 0
