# Licensed under CC BY-NC-SA 4.0
import json

class HADiscovery:
    """Handles Home Assistant MQTT Discovery for OpenERV."""
    
    def __init__(self, client, node_id, model="TW4"):
        self.client = client
        self.node_id = node_id
        self.model = model
        self.base_topic = f"openerv/{node_id}"
        self.discovery_prefix = "homeassistant"

    def publish_config(self):
        """Publish discovery configurations for all entities."""
        self._publish_fan()
        self._publish_sensor("pressure", "Pressure", "Pa", "pressure")
        self._publish_sensor("temperature", "Temperature", "°C", "temperature")

    def _publish_fan(self):
        topic = f"{self.discovery_prefix}/fan/{self.node_id}/config"
        payload = {
            "name": f"OpenERV {self.model}",
            "unique_id": f"{self.node_id}_fan",
            "state_topic": f"{self.base_topic}/fan/state",
            "command_topic": f"{self.base_topic}/fan/set",
            "pct_stat_t": f"{self.base_topic}/fan/speed/state",
            "pct_cmd_t": f"{self.base_topic}/fan/speed/set",
            "device": self._device_info()
        }
        self.client.publish(topic, json.dumps(payload).encode())

    def _publish_sensor(self, sensor_id, name, unit, device_class):
        topic = f"{self.discovery_prefix}/sensor/{self.node_id}_{sensor_id}/config"
        payload = {
            "name": f"OpenERV {name}",
            "unique_id": f"{self.node_id}_{sensor_id}",
            "state_topic": f"{self.base_topic}/{sensor_id}/state",
            "unit_of_meas": unit,
            "device_class": device_class,
            "device": self._device_info()
        }
        self.client.publish(topic, json.dumps(payload).encode())

    def _device_info(self):
        return {
            "identifiers": [self.node_id],
            "name": f"OpenERV {self.node_id}",
            "model": self.model,
            "manufacturer": "OpenERV"
        }

    def update_state(self, pressure, temperature, fan_speed):
        """Publish current state to MQTT."""
        self.client.publish(f"{self.base_topic}/pressure/state", str(pressure).encode())
        self.client.publish(f"{self.base_topic}/temperature/state", str(temperature).encode())
        self.client.publish(f"{self.base_topic}/fan/speed/state", str(int(fan_speed)).encode())
        self.client.publish(f"{self.base_topic}/fan/state", b"ON" if fan_speed > 0 else b"OFF")
