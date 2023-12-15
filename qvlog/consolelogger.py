from . import Level, LoggingVars, Logging

from . import Logger

import tkinter as tk
import threading

class ConsoleLogger():
    __instance = None

    @staticmethod
    def Get(name = None, path = None, level = None, cout = None, fout = None, overwrite = None):
        if ConsoleLogger.__instance is None:
            ConsoleLogger.__instance = ConsoleLogger(name, path, level, cout, fout, overwrite)
        return ConsoleLogger.__instance

    def __init__(self, name, path, level, cout, fout, overwrite):
        if ConsoleLogger.__instance is not None:
            raise Exception("ProcessLogger attempted re-init")
        lv = LoggingVars(name, name, level, cout, fout, overwrite)
        lv.Path(path)
        self.log = Logging(lv)
        self.queue = []
        self.queueLock = threading.Lock()
        self.thread = threading.Thread(target=self.start)
        self.SetLevels()
        self.after(5, self.on_idle)

    def start(self):
        self.thread.start()

    def _start(self):
        root = tk.Tk()
        self.frame = tk.Frame(root)
        self.text = tk.Text(self.frame, bg="black", fg="white")
        self.text.pack()
        self.frame.pack()
        root.mainloop()

    def on_idle(self):
        with self.queueLock:
            for msg in self.queue:
                self.text.insert(tk.END, msg)
                self.text.see(tk.END)
            self.queue = []
        self.after(5, self.on_idle)

    def show(self, msg, sep="\n"):
        with self.queueLock:
            self.queue.append(str(msg) + sep)

    def __exit__(self):
        self.process.communicate("Bye!\n")

    def SetLevels(self):
        for lvl in Level:
            setattr(self, lvl.name.lower(), getattr(self.log, lvl.name.lower()))