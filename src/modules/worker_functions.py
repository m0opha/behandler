import subprocess
import time

def _bluetoothctl_command(commands):

    process = subprocess.Popen(
        ['bluetoothctl'], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

    for cmd in commands:
        process.stdin.write(cmd + '\n')
        process.stdin.flush()
        time.sleep(1)

    process.stdin.write('exit\n')
    process.stdin.flush()

    output, errors = process.communicate()
    return output