import argparse
import sys

from .modules import *

def main():
    parser = argparse.ArgumentParser(
        usage="behandler [-c [INDEX]] [-d] [-s][-r]",
        description="Bluetooth device handler",
        formatter_class=HelpFormatter
    )
    
    parser.add_argument('--connect','-c', nargs='?', const=True, default=False, type=int,help="connect device by index.")
    parser.add_argument('--disconnect', '-d', action='store_true', help="disconnect device")
    parser.add_argument('--scan', '-s' ,action='store_true' , help="scan avalible bluetooth devices")
    parser.add_argument('--remove' , "-r", action='store_true', help="remove bluetooth device")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    
    devices = getAllBluetoothDevices()
    current_device = getCurrentDeviceName()

    device_name = ""
    mac_address = ""

    if current_device:
        (device_name, mac_address), = current_device.items()
    
    # Remove bluetooth device
    if args.remove:
        
        if len(devices) == 0:
            pWarning("[*] No bluetooth devices found")
            return

        for _index, (_name , _mac) in enumerate(devices.items()):
            print(f"[{_index}] {_name}")
        
        option = input(f"> ")

        if not option.isdigit():
            pError("[-] Selection must be a digit")
        
        option = int(option)
        if len(devices) <= option:
            pError("[-] Out of range.")

        device_name = list(devices.keys())[option]
        if removeDevice(devices[device_name]):
            pWarning("[*] Removed device ", no_salt=True)
            print(device_name)
            return

        pError("[-] Not removed device" , no_salt=True)
        print(device_name)
        return

    # Pair bluetooth device and connect
    if args.scan:
        scan_data = scanner_interface()
        if not scan_data:
            pError("[-] Scan failed")
            return
        
        mac_address , device_name = scan_data 
        pairBluetoothDevice(mac_address)
        connect(mac_address, device_name)
        return
            
    # Disconnect
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

    # Automatic connection
    if args.connect is True:
        if not devices:
            pWarning("[!] No Bluetooth devices register.")
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
        return

    if len(devices) >= args.connect:
        device_name, mac_address = next(iter(devices.items()))
        connect(mac_address, device_name)
        return        
    
    else:
        pError("[!] No device found.")
        return

