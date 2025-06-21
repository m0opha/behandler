import subprocess
import threading
from threading import Lock

from .utils import *

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
        

def scanner_interface():
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
