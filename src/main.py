import argparse
import sys

from .modules import *

def main():
    devices = getAllBluetoothDevices()
    current_device = getCurrentDeviceName()

    device_name = ""
    mac_address = ""

    if current_device:
        (device_name, mac_address), = current_device.items()
    parser = argparse.ArgumentParser(
        usage="behandler [-c [INDEX]] [-d] [-s]",
        description="Bluetooth device handler",
        formatter_class=HelpFormatter
    )
    
    parser.add_argument('--connect','-c', nargs='?', const=True, default=False, type=int,
                        help="connect device by index.")
    
    parser.add_argument('--disconnect', '-d', action='store_true', help="disconnect device")

    parser.add_argument('--scan', '-s' ,action='store_true' , help="scan avalible bluetooth devices")
    
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    
    #scan and connect bluetooth devices
    if args.scan:
        scan_data = scanner_interface()
        if not scan_data:
            pError("[-]Scanner error")
            return
        
        mac_address , device_name = scan_data 
        pairBluetoothDevice(mac_address)
        connect(mac_address, device_name)
        return
            
    # Desconectar
    if args.disconnect:
        if device_name == "":
            pWarning("[!] There is no active Bluetooth connection.")
            return

        disconnect(device_name, mac_address)
        return

    # Already connected
    if device_name != "":
        pWarning(f"[!] Already connected to ", no_salt=True )
        print(device_name)
        return

    #automate connect
    if args.connect is True:
        if not devices:
            pWarning("[!] No Bluetooth devices registered.")
            return

        if len(devices) == 1:
            device_name, mac_address = list(devices.items())[0]
            connect(mac_address, device_name)
            return

        print("Select Bluetooth device:")
        for index, (device_name, _) in enumerate(devices.items()):
            print(f"[{index}] {device_name}")

        selected_device = input("> ")
        if not selected_device.isdigit():
            pError("[-] Selection must be a digit.")
            return

        selected_device = int(selected_device)
        if selected_device >= len(devices):
            pError("[-] Selection out of range.")
            return
        
        device_name, mac_address = list(devices.items())[selected_device]
        connect(mac_address, device_name)
        setBluetoothAudio()
        return

    if len(devices) >= args.connect:
        device_name, mac_address = next(iter(devices.items()))
        connect(mac_address, device_name)
        return        
    else:
        pError("[!] No device found.")
        return
