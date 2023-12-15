from . import Level, LoggingVars, Logging

class Logger:
    __instance = None

    @staticmethod
    def Get(name = None, path = None, level = None, cout = None, fout = None, overwrite = None):
        if Logger.__instance is None:
            Logger.__instance = Logger(name, path, level, cout, fout, overwrite)
        return Logger.__instance
    
    def __init__(self, name, path, level, cout, fout, overwrite):
        if Logger.__instance is not None:
            raise Exception("Logger attempted re-init")
        lv = LoggingVars(name, name, level, cout, fout, overwrite)
        lv.Path(path)
        self.log = Logging(lv)
        self.SetLevels()

    def SetLevels(self):
        for lvl in Level:
            setattr(self, lvl.name.lower(), getattr(self.log, lvl.name.lower()))

    def Child(self, name: str):
        log = _Logger(self.log.lv.Child(name))
        setattr(self, name, log)
        return log

    def Sibling(self, name: str):
        log = _Logger(self.log.lv.Sibling(name))
        setattr(self, name, log)
        return log

class _Logger(Logger):
    @staticmethod
    def Get():
        raise NotImplementedError("_Logger is not implemented")
    
    def __init__(self, lv: LoggingVars):
        self.log = Logging(lv)
        self.SetLevels()
    