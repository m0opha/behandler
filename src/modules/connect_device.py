import subprocess

from .colors import pSuccess, pError

def connect(mac_address, device_name):
    command = ["bluetoothctl" , "connect", mac_address]
    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )

    if result.returncode != 1:
        pSuccess(f"[+] Connected to ", no_salt=True)
        print(device_name)
        return True
    
    pError(f"[-] Failed to connect to ", no_salt=True) 
    print(device_name)
    return False