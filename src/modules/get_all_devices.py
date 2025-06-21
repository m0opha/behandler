import subprocess
import json

def getAllBluetoothDevices():
    command = ["bluetoothctl", "devices"]
    result = subprocess.run(
        command, 
        capture_output=True, 
        text=True
    )
    all_devices = result.stdout.split("\n")
    
    found_devices = {}
    for device in all_devices:
        row_data = device.split(" ")

        if [''] == row_data:
            continue

        mac_address = row_data[1]
        device_name = " ".join(row_data[2:])

        found_devices[device_name] = mac_address
        
    return found_devices

if __name__ == "__main__":
    print(
        json.dumps(
            getAllBluetoothDevices(),
            indent=2)
    )
