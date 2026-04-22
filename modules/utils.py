#!/usr/bin/env python3

import subprocess
import re
import shutil
import termios
import tty
import json
import select
import sys

from vars.setup import _TEST, space_TEST
from modules.test import test

def execute(
        cmd: str, 
        input: str = None,
        return_output = False,
        _TEST = False
        ) -> bool:
    
    cmd = list(cmd.split(" "))

    result = subprocess.run(
        cmd,
        #shell=True,
        capture_output=True,
        text=True,
        input=input
    )

    if _TEST:
        print(f"{space_TEST}Command: {" ".join(cmd)}")
        print(f"{space_TEST}stdout: {len(result.stdout.strip("\n"))}")
        print(f"{space_TEST}stderr: {len(result.stderr)}")
        print(f"{space_TEST}returncode: {result.returncode}")

    if return_output and result.returncode == 0:
        return result.stdout.strip("\n")

    return result.returncode == 0


def datatodict(
        chrsplit: str = "=",
        data: str = "",
        _TEST=False
        ):
    
    builddict = {}
    
    listToWork = data.split("\n")

    for _item in listToWork:
    
        if _TEST:
            print(_item)
            print(_item.split(chrsplit))

        if _item.strip() == "":
            continue

        # limpiar tabs
        _item = _item.replace("\t", "")

        if chrsplit in _item:
            key, value = _item.split(chrsplit, 1)
        else:
            rd = _item.split(" ", 1)
            key = rd[0]
            value = rd[1] if len(rd) > 1 else ""

        builddict[key.strip()] = value.strip()

    if _TEST:
        print(json.dumps(builddict, indent=2))

    return builddict



def printAt(row, col, text):
    term_rows, term_cols = shutil.get_terminal_size()

    # Convertir índices negativos: -1 => última fila/columna
    if row < 0:
        row = term_rows + row + 1
    
    if col < 0:
        col = term_cols + col + 1

    # Limitar a rango válido ANSI (empiezan en 1)
    row = max(1, min(row, term_rows))
    col = max(1, min(col, term_cols))

    print(f"\033[{row};{col}H{text}", end='', flush=True)



def clean_string(line):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    line = ansi_escape.sub('', line)
    control_chars = ''.join(map(chr, range(0, 32)))
    control_char_re = re.compile(f'[{re.escape(control_chars)}]')
    return control_char_re.sub('', line).strip()



class TerminalRawMode:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None

    def __enter__(self):
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)

        # Guardar pantalla y limpiar
        sys.stdout.write("\033[?1049h\033[2J\033[H")  # save screen + clear
        sys.stdout.write("\033[?25l")  # ocultar cursor
        sys.stdout.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

        # Restaurar pantalla y mostrar cursor
        sys.stdout.write("\033[?1049l\033[?25h")  # restore screen + show cursor
        sys.stdout.flush()


def getch(timeout=0):
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if not rlist:
        return None  # no hay tecla presionada

    ch1 = sys.stdin.read(1)
    if ch1 != '\x1b':
        return ch1
    
    ch2 = sys.stdin.read(2)
    return ch1+ch2

###########################################
#           TESTING.........
###########################################
_TOTEST = [
    # fun        test_status   args                            _TEST
    [execute,    0,            ("echo \'testing this fun.\'",  False)],
    [datatodict, 0,            ("=","1=1\n2=2\n3=3",           True )]    
]

if __name__ == "__main__":
    if _TEST:
        test(_TOTEST)