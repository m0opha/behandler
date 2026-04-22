#!/usr/bin/env python3
import json

from vars.commands import cmd_bluetoothctl_show, cmd_bluetoothctl_poweron, cmd_bluetoothctl_agent
from vars.setup import _TEST, space_TEST
from modules.test import test
from modules.utils import execute, datatodict


def data_bluetoothctl(_TEST=False):
    cmd_stdout = execute(
        cmd_bluetoothctl_show,
        return_output=True
    )

    if cmd_stdout is False:
        return False

    if _TEST:
        print(cmd_stdout)

    bluetoothctl_data = datatodict(":", cmd_stdout)

    bluetoothctl_data = {
        k.replace("\t", "").strip(): v.strip()
        for k, v in bluetoothctl_data.items()
    }

    if _TEST:
        print(json.dumps(bluetoothctl_data, indent=2))

    return bluetoothctl_data


def verify_bluetoothctl():
    config = data_bluetoothctl()

    if config.get("Powered") != "yes":
        if execute(cmd_bluetoothctl_poweron):
            print("[*] Bluetooth power on.")
        else:
            print("[!] Failed to power on bluetooth.")

    if execute(cmd_bluetoothctl_agent):
        print("[*] Agent enabled and set as default.")
    else:
        print("[!] Failed to enable agent.")



###########################################
#           TESTING.........
###########################################
_TOTEST = [
    # fun                 test_status     args
    [data_bluetoothctl,   0,              (True,)],
    [verify_bluetoothctl, 1,              ()]
    ]

if __name__ == "__main__":
    if _TEST:
        test(_TOTEST)