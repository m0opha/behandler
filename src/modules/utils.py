import argparse
import re
import sys
import termios
import tty
import shutil
import select

class HelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            return super()._format_action_invocation(action)

        if action.nargs == 0:
            return ', '.join(action.option_strings)

        return ', '.join(action.option_strings)

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        return ''
    
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
        
def clean_string(line):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    line = ansi_escape.sub('', line)
    control_chars = ''.join(map(chr, range(0, 32)))
    control_char_re = re.compile(f'[{re.escape(control_chars)}]')
    return control_char_re.sub('', line).strip()

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

def getch(timeout=0):
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if not rlist:
        return None  # no hay tecla presionada

    ch1 = sys.stdin.read(1)
    if ch1 != '\x1b':
        return ch1
    
    ch2 = sys.stdin.read(2)
    return ch1+ch2
