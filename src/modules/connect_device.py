import subprocess

from .colors import pSuccess, pError
import subprocess

def connect(mac_address, device_name, timeout=30):
    command = ["bluetoothctl", "connect", mac_address]
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        pError(f"[-] Timeout connecting to {device_name}")
        return False

    if result.returncode != 1:
        pSuccess(f"[+] Connected to ", no_salt=True)
        print(device_name)
        return True

    pError(f"[-] Failed to connect to ", no_salt=True)
    return False
