# Licensed under CC BY-NC-SA 4.0
import socket
import time
import json
import machine

class ProvisioningManager:
    """Manages the captive portal for WiFi provisioning."""
    
    HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>OpenERV Setup</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: sans-serif; margin: 2em; background: #f0f0f0; }}
        .container {{ background: white; padding: 2em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        label {{ display: block; margin-top: 1em; }}
        input, select {{ width: 100%; padding: 0.5em; margin-top: 0.2em; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }}
        button {{ margin-top: 1.5em; padding: 0.7em 1.5em; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background: #0056b3; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>OpenERV Setup</h1>
        <p>Configure the device to connect to your local WiFi network.</p>
        <form method="POST" action="/save">
            <label for="ssid">WiFi Name (SSID)</label>
            <input type="text" id="ssid" name="ssid" required placeholder="e.g. MyHomeWiFi">
            
            <label for="password">WiFi Password</label>
            <input type="password" id="password" name="password" required>
            
            <label for="role">Device Role</label>
            <select id="role" name="role">
                <option value="leader">Leader (Main Control)</option>
                <option value="follower">Follower (Secondary Module)</option>
            </select>

            <button type="submit">Save and Reboot</button>
        </form>
    </div>
</body>
</html>
"""

    def __init__(self, network_manager):
        self.net = network_manager

    def start_server(self, ip):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.settimeout(1.0)
        s.bind(addr)
        s.listen(1)
        print(f"Provisioning server listening on http://{ip}")

        while True:
            try:
                cl, addr = s.accept()
                print(f"Client connected from {addr}")
                request = cl.recv(1024).decode()
                
                if "POST /save" in request:
                    self._handle_save(cl, request)
                    time.sleep(2)
                    machine.reset()
                else:
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(self.HTML_TEMPLATE)
                    cl.close()
            except Exception:
                if self.net.wdt: self.net.wdt.feed()
                continue

    def _handle_save(self, cl, request):
        # Extract POST body
        try:
            body = request.split('\r\n\r\n')[1]
            params = {}
            for pair in body.split('&'):
                key, value = pair.split('=')
                # Simple URL decoding for + space
                params[key] = value.replace('+', ' ').replace('%21', '!').replace('%40', '@').replace('%23', '#')
            
            # Load current config
            config = {}
            try:
                with open("persistent_vars.json", "r") as f:
                    config = json.load(f)
            except: pass
            
            # Update credentials
            config["ssid_main_wifi"] = params.get("ssid")
            config["password_main_wifi"] = params.get("password")
            config["leader_or_follower"] = params.get("role", "leader")
            
            with open("persistent_vars.json", "w") as f:
                json.dump(config, f)
            
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send("<html><body><h1>Config Saved!</h1><p>Rebooting... wait 10 seconds then check your router.</p></body></html>")
            cl.close()
            print("Configuration updated successfully.")
        except Exception as e:
            print(f"Error saving config: {e}")
            cl.send('HTTP/1.0 500 Internal Server Error\r\n\r\n')
            cl.close()
