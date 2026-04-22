import subprocess

from modules.utils import execute
from vars.commands import cmd_bluetoothctl_devices, cmd_bluetoothctl_info

def getDevices():

    devices_found = execute(
        cmd=cmd_bluetoothctl_devices,
        return_output=True
        )
    devices_found = devices_found.spli("\n")

    fd = {}
    for device in devices_found:
        row_data = device.split(" ")

        if [''] == row_data:
            continue

        mac_address = row_data[1]
        device_name = " ".join(row_data[2:])

        fd[device_name] = mac_address
        
    return fd

def currentDevice():

    result = subprocess.run(
        cmd_bluetoothctl_info,
        capture_output=True,
        text=True
    )

    if result.returncode == 1:
        return False
    
    row_data = result.stdout.strip().split("\n")

    mac_device = row_data[0].split(" ")[1]
    device_name = row_data[1].split(":")[1].strip()
    
    return{device_name : mac_device}

def connectDevice(mac_address, device_name, timeout=30):
    command = ["bluetoothctl", "connect", mac_address]
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        print(f"[-] Timeout connecting to", no_salt=True)
        print(device_name)
        return False

    if result.returncode != 1:
        print(f"[+] Connected to ",device_name)
        return True

    print("[!] Was not connect to ",device_name)
    return False