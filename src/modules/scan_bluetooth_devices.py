import subprocess
import threading
import re
import sys
import termios
import tty
from threading import Lock
import shutil
import select

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

def clean_string(line):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    line = ansi_escape.sub('', line)
    control_chars = ''.join(map(chr, range(0, 32)))
    control_char_re = re.compile(f'[{re.escape(control_chars)}]')
    return control_char_re.sub('', line).strip()

class BluetoothScanner:

    def __init__(self):
        self.devices = {}
        self.running = False
        self.process = None
        self.lock = Lock()
        self.thread = None
    
    def start(self):        
        self.process = subprocess.Popen(
            ['bluetoothctl'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        self.running = True
        
        self.process.stdin.write('scan on\n')
        self.process.stdin.flush()
        
        self.thread = threading.Thread(target=self._read_output, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write('scan off\n')
                self.process.stdin.flush()
            except Exception:
                pass
            self.process.terminate()
            self.process.wait()

        if self.thread:
            self.thread.join()

    def _read_output(self):
        while self.running:
            raw_line = self.process.stdout.readline()
            if not raw_line:
                break
            
            line = clean_string(raw_line)
            if not line:
                continue

            if line.startswith("[NEW]"):
                parts = line.split()
                if len(parts) >= 4:
                    mac = parts[2]
                    name = " ".join(parts[3:])
                    with self.lock:
                        self.devices[mac] = name

            elif line.startswith("[DEL]"):
                parts = line.split()
                if len(parts) >= 3:
                    mac = parts[2]
                    with self.lock:
                        self.devices.pop(mac, None)
                    
    def getDevices(self):
        with self.lock:
            if not self.devices:
                return None
            return dict(self.devices)
        
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

def scanBluetoothDevices():
    scanner = BluetoothScanner()
    prev_items = []
    prev_selection = -1
    selection = 0

    with TerminalRawMode():
        scanner.start()
        try:
            while True:
                devices = scanner.getDevices()
                items = list(devices.items()) if devices else []

                # Limitar selection al rango válido
                if selection >= len(items):
                    selection = max(0, len(items) - 1)
                if selection < 0:
                    selection = 0

                # Actualizar pantalla solo si cambió lista o selección
                if items != prev_items or selection != prev_selection:
                    # Limpiar líneas previas
                    for i in range(max(len(prev_items), len(items))):
                        printAt(3 + i, 0, "\033[2K")

                    # Imprimir lista con selector
                    for i, (mac, name) in enumerate(items):
                        prefix = "> " if i == selection else "  "
                        printAt(3 + i, 0, f"{prefix}{mac} : {name}")

                    prev_items = items
                    prev_selection = selection

                printAt(1, 0, "Scanning Bluetooth devices (Ctrl+C to exit, Enter to select)...")
                printAt(2, 0, "Use ↑ ↓ to navigate, Enter to select, Ctrl+C to exit.")

                key = getch()

                if key is None:
                    continue

                if key == '\x03':  # Ctrl+C
                    return None

                if key == '\r' or key == '\n':  # Enter
                    if items:
                        selected_device = items[selection]
                        return selected_device

                if key == '\x1b[A':  # Flecha arriba
                    if selection > 0:
                        selection -= 1
                    continue

                if key == '\x1b[B':  # Flecha abajo
                    if selection < len(items) - 1:
                        selection += 1
                    continue
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            scanner.stop()
