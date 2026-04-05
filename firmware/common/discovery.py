# Licensed under CC BY-NC-SA 4.0
import json
import machine
import ubinascii

class MQTTDiscovery:
    """Handles Home Assistant MQTT Discovery for OpenERV."""
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.device_id = self._get_unique_id()
        self.base_topic = f"openerv/{self.device_id}"
        self.discovery_prefix = "homeassistant"

    def _get_unique_id(self):
        try:
            return ubinascii.hexlify(machine.unique_id()).decode()
        except:
            return "unknown_dev"

    def publish_configs(self):
        """Publishes HA discovery payloads for all entities."""
        device_info = {
            "identifiers": [self.device_id],
            "name": f"OpenERV {self.config.get('leader_or_follower', 'Unit').capitalize()}",
            "model": "TW4/WM12",
            "manufacturer": "OpenERV"
        }

        # 1. CO2 Sensor
        if self.config.get('enable_co2'):
            self._publish_sensor_config("co2", "CO2", "carbon_dioxide", "ppm", device_info)
            self._publish_sensor_config("humidity", "Humidity", "humidity", "%", device_info)
            self._publish_sensor_config("temperature", "Internal Temperature", "temperature", "°C", device_info)

        # 2. Pressure Sensor (SDP810)
        self._publish_sensor_config("pressure", "Differential Pressure", "pressure", "Pa", device_info)

        # 3. Climate Entity (for mode and target speed)
        self._publish_climate_config(device_info)

    def _publish_sensor_config(self, sensor_type, name, device_class, unit, device_info):
        topic = f"{self.discovery_prefix}/sensor/{self.device_id}_{sensor_type}/config"
        payload = {
            "name": f"{device_info['name']} {name}",
            "stat_t": f"{self.base_topic}/state",
            "unit_of_meas": unit,
            "dev_cla": device_class,
            "val_tpl": f"{{{{ value_json.{sensor_type} | round(2) }}}}",
            "uniq_id": f"{self.device_id}_{sensor_type}",
            "dev": device_info
        }
        self.client.publish(topic, json.dumps(payload))

    def _publish_climate_config(self, device_info):
        topic = f"{self.discovery_prefix}/climate/{self.device_id}_hvac/config"
        payload = {
            "name": device_info['name'],
            "stat_t": f"{self.base_topic}/state",
            "mode_stat_t": f"{self.base_topic}/mode_state",
            "mode_cmd_t": f"{self.base_topic}/mode_set",
            "temp_stat_t": f"{self.base_topic}/state",
            "temp_val_tpl": "{{ value_json.temperature }}",
            "modes": ["fan_only", "heat_cool", "off"],
            "fan_modes": ["low", "medium", "high", "boost"],
            "fan_mode_stat_t": f"{self.base_topic}/fan_state",
            "fan_mode_cmd_t": f"{self.base_topic}/fan_set",
            "uniq_id": f"{self.device_id}_climate",
            "dev": device_info
        }
        # Mapping: 
        # heat_cool -> Heat Recovery (Normal)
        # fan_only -> Free Cooling (No reversal)
        # off -> Shutdown
        self.client.publish(topic, json.dumps(payload))

    def update_state(self, state_dict):
        """Publishes the current state to the state topic."""
        self.client.publish(f"{self.base_topic}/state", json.dumps(state_dict))

    def update_mode(self, mode):
        self.client.publish(f"{self.base_topic}/mode_state", mode)

    def update_fan_mode(self, fan_mode):
        self.client.publish(f"{self.base_topic}/fan_state", fan_mode)
