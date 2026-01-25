import subprocess

def removeDevice(mac):

    command=['bluetoothctl', "remove" , mac]

    result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

    if result.returncode == 1:
        return False

    return True
