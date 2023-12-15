import socket
import threading

import sys
import os
import time
from subprocess import Popen
import signal

import random

from .logging import LoggingVars, Logging, Level
from .logger import Logger, _Logger

class SocketLogger(Logger):
    __instance = None

    @staticmethod
    def Get(name = None, path = None, level = None, cout = None, fout = None, overwrite = None):
        if SocketLogger.__instance is None:
            SocketLogger.__instance = SocketLogger(name, path, level, cout, fout, overwrite)
        return SocketLogger.__instance

    def __init__(self, name, path, level, cout, fout, overwrite):
        if SocketLogger.__instance is not None:
            raise Exception("SocketLogger attempted re-init")
        lv = LoggingVars(name, name, level, False, fout, overwrite)
        lv.Path(path)
        self.log = Logging(lv)
        self.port = self._selectPort()
        self.SetLevels()
        self._Setup()

    def __del__(self):
        os.remove(f"temp_socket.py")

    def SetLevels(self):
        for lvl in Level:
            setattr(self, lvl.name.lower(), lambda msg,self=self,lvl=lvl: self.Log(lvl, msg))

    def _selectPort(self):
        while True:
            for port in [random.randint(1024, 65535) for _ in range(50)]:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    result = s.connect_ex(("localhost", port)) == 0
                    print(f"Port {port} got {not result}")
                    if not result:
                        return port
                    
    def _Setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print(f"Binding to port {self.port}")
        self.sock.bind(("localhost", self.port))
        with open("temp_socket.py", "w+") as f:
            f.write("import socket\n")
            f.write("import os\n")
            #f.write("time.sleep(500)\n")
            f.write("sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
            f.write(f"print('Connecting to {self.port}...', end='\\r')\n")
            f.write(f"sock.connect(('localhost', {self.port}))\n")
            f.write(f"print(f'Successfully connected on port {self.port}!')\n")
            f.write("while True:\n")
            f.write("    data = sock.recv(1024).decode('UTF-8')\n")
            f.write("    if data:\n")
            f.write("        print(data)\n")
            f.write("    if not os.path.exists('temp_socket.py'):\n")
            f.write("        break\n")
            f.write("sock.close()\n")
            f.write("input('Press enter to exit')\n")
        time.sleep(1.5)
        #print(f"File was written!")
        threading.Thread(target=self._LaunchReceive).start()
        self._ClientWait()
        #print(f"Client connected!")

    def _ClientWait(self):
        #print(f"Waiting for client...")
        self.sock.listen(1)
        self.client, _ = self.sock.accept()

    def Log(self, level, message):
        getattr(self.log, level.name.lower())(message)
        self.Send(f"{self.log._header(level)}: {message}")

    def Send(self, msg):
        self.client.send(msg.encode("UTF-8"))
                    
    def _LaunchReceive(self):
        #print(f"Launching sub-console...")
        self.receiver = Popen(["cmd.exe", "/c", "start", sys.executable, "temp_socket.py"])