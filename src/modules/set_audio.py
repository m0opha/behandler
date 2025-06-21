import subprocess

def setBluetoothAudio():
    #i dont know why this works!
    command = ["pactl", "list", "short","sinks"]
    result = subprocess.run(
        command, 
        shell=True, 
        text=True, 
        capture_output=True
    ).stdout.strip()
    
    if result.returncode != 1:
        return False
    
    return True

