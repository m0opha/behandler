import argparse
import sys

from verify_bluetoothctl import verify_bluetoothctl

def main():
    parser = argparse.ArgumentParser(
        usage="behandler [-c [INDEX]] [-d] [-s][-r]",
        description="Bluetooth device handler",
    )
    
    parser.add_argument(
        '--connect','-c',
          nargs='?', 
          const=True, 
          default=False, 
          type=int,
          help="connect device by index."
          )
    parser.add_argument(
        '--disconnect', '-d', 
        action='store_true', 
        help="disconnect device"
        )
    parser.add_argument(
        '--scan', '-s' ,
        action='store_true', 
        help="scan avalible bluetooth devices"
        )
    parser.add_argument(
        '--remove' , "-r", 
        action='store_true', 
        help="remove bluetooth device"
        )

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    verify_bluetoothctl()

    # Remove bluetooth device
    if args.remove:
        pass
    
    # Pair bluetooth device and connect
    if args.scan:
        pass

    # Disconnect
    if args.disconnect:
        pass

    # Automatic connection
    if args.connect:
        pass

if __name__ == "__main__":
    main()