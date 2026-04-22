#!/usr/bin/env python3

import subprocess
import re
import shutil
import termios
import tty
import json
import select
import sys

try:
    from colorama import Fore, Back, Style

except ImportError:
    print("Is required install colorama in the system.")    
    sys.exit(1)

def execute(cmd:str, input:str = None, return_output:bool = False) -> bool:
    
    cmd = list(cmd.split(" "))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input
    )

    if return_output:
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


def clean_string(string:str):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    string = ansi_escape.sub('', string)
    control_chars = ''.join(map(chr, range(0, 32)))
    control_char_re = re.compile(f'[{re.escape(control_chars)}]')
    return control_char_re.sub('', string).strip()


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

def printSuccess(text, salt=True):
    print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}", end="" if not salt else "\n")

def printError(text, salt=True):
    print(f"{Style.BRIGHT}{Fore.RED}{text}{Style.RESET_ALL}", end="" if not salt else "\n")