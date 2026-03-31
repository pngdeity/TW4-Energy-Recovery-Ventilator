import pytest
import json
from ha_discovery import HADiscovery

class MockMQTTClient:
    def __init__(self):
        self.published = []
    def publish(self, topic, payload):
        self.published.append((topic, payload))

def test_ha_discovery_init():
    client = MockMQTTClient()
    ha = HADiscovery(client, "test_pico", "TW4")
    assert ha.node_id == "test_pico"
    assert ha.base_topic == "openerv/test_pico"

def test_publish_config():
    client = MockMQTTClient()
    ha = HADiscovery(client, "test_pico", "TW4")
    ha.publish_config()
    
    # Check for fan config
    payload_bytes = next(p for t, p in client.published if "fan/test_pico/config" in t)
    payload = json.loads(payload_bytes.decode())
    assert payload["name"] == "OpenERV TW4"
    assert payload["unique_id"] == "test_pico_fan"
    
    # Check for sensors
    assert any("sensor/test_pico_pressure/config" in t for t, p in client.published)
    assert any("sensor/test_pico_temperature/config" in t for t, p in client.published)

def test_update_state():
    client = MockMQTTClient()
    ha = HADiscovery(client, "test_pico", "TW4")
    ha.update_state(15.5, 22.1, 50)
    
    # Verify published states
    assert ("openerv/test_pico/pressure/state", b"15.5") in client.published
    assert ("openerv/test_pico/temperature/state", b"22.1") in client.published
    assert ("openerv/test_pico/fan/speed/state", b"50") in client.published
    assert ("openerv/test_pico/fan/state", b"ON") in client.published
