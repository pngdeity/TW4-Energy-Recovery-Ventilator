# Licensed under CC BY-NC-SA 4.0
import os
import uhashlib
import ubinascii
import machine

class OTAManager:
    """Manages OTA updates for python-level firmware files."""
    
    def __init__(self, base_url="http://ota.openerv.org/latest"):
        self.base_url = base_url
        self.manifest_file = "ota_manifest.json"

    def verify_file(self, filename, expected_hash):
        """Verifies a file against a SHA256 hash."""
        try:
            with open(filename, "rb") as f:
                h = uhashlib.sha256()
                while True:
                    chunk = f.read(1024)
                    if not chunk: break
                    h.update(chunk)
                digest = ubinascii.hexlify(h.digest()).decode()
                return digest == expected_hash
        except:
            return False

    def stage_update(self, filename, content, expected_hash):
        """Stages a new file version with a .new suffix."""
        temp_name = filename + ".new"
        try:
            with open(temp_name, "wb") as f:
                f.write(content)
            
            if self.verify_file(temp_name, expected_hash):
                return True
            else:
                os.remove(temp_name)
                return False
        except:
            return False

    def finalize_update(self, file_list):
        """Swaps staged files and reboots. This is the 'dual-bank' logic at file level."""
        try:
            # 1. Verify all .new files exist
            for f in file_list:
                if not f + ".new" in os.listdir():
                    return False
            
            # 2. Swap
            for f in file_list:
                if f in os.listdir():
                    os.rename(f, f + ".old")
                os.rename(f + ".new", f)
            
            # 3. Reboot
            print("OTA Update finalized. Rebooting...")
            machine.reset()
        except Exception as e:
            print(f"Finalize failed: {e}")
            return False

    def rollback(self, file_list):
        """Rolls back to .old files if update fails."""
        for f in file_list:
            if f + ".old" in os.listdir():
                if f in os.listdir():
                    os.remove(f)
                os.rename(f + ".old", f)
        machine.reset()
