# Licensed under CC BY-NC-SA 4.0
import socket
import struct
import time
import select

class SyncManager:
    """Handles UDP synchronization and pressure balance offsets between Leader and Follower."""
    
    UDP_PORT = 5005
    # Packet format: ! L f (Unsigned Long for ticks_ms, Float for pressure_offset)
    PACKET_FMT = "!Lf"

    def __init__(self, config, wdt=None):
        self.config = config
        self.wdt = wdt
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        
        if self.config['leader_or_follower'] == "leader":
            # Leader sends to Follower
            self.target_ip = self.config['ip_follower']
        else:
            # Follower listens
            self.sock.bind(('0.0.0.0', self.UDP_PORT))

    def send_sync(self, current_ticks, pressure_offset):
        """Leader sends sync packet."""
        if self.config['leader_or_follower'] != "leader":
            return
            
        try:
            packet = struct.pack(self.PACKET_FMT, current_ticks, pressure_offset)
            self.sock.sendto(packet, (self.target_ip, self.UDP_PORT))
        except Exception as e:
            print(f"Sync send error: {e}")

    def receive_sync(self):
        """Follower receives sync packet. Returns (ticks_ms, pressure_offset) or (None, None)."""
        if self.config['leader_or_follower'] == "leader":
            return None, None
            
        try:
            r, _, _ = select.select([self.sock], [], [], 0)
            if r:
                data, addr = self.sock.recvfrom(1024)
                ticks, offset = struct.unpack(self.PACKET_FMT, data)
                return ticks, offset
        except Exception as e:
            # print(f"Sync receive error: {e}")
            pass
        return None, None
