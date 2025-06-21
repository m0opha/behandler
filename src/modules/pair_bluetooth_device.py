import subprocess

def pairBluetoothDevice(mac_address):
    command = ["bluetoothctl", "pair", mac_address]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return False
    
    return True