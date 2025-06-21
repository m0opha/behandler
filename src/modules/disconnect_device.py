import subprocess

from .colors import pWarning, pError

def disconnect(device_name , mac_address):
    command = ["bluetoothctl", "disconnect" , mac_address]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        pError(f"[-] Fail trying to disconnect ", no_salt=True) 
        print(device_name)
        return False
    

    pWarning(f"[!] Disconnected to ", no_salt=True)
    print(device_name)
    return True