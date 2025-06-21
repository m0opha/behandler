import subprocess

def getCurrentDeviceName():
    no_current_device_output = "Missing device address argument"
    command=["bluetoothctl","info"]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    if result.stdout.strip() == no_current_device_output:
        return False
    
    row_data = result.stdout.strip().split("\n")
    mac_device = row_data[0].split(" ")[1]
    device_name = row_data[1].split(":")[1].strip()
    
    return{device_name : mac_device}