from enum import Enum
import datetime as dt

from os import makedirs

class Level(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 5

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

class LoggingVars:
    def __init__(self, name = None, file = None, level = None, cout = None, fout = None, overwrite = None):
        self._path = f"logs"
        self.name: str       = None
        self.file: str       = None
        self.level: Level    = Level.INFO
        self.cout: bool      = False
        self.fout: bool      = True
        self.overwrite: bool = True
        self.Init(name, file, level, cout, fout, overwrite)

    def __str__(self):
        fmt = f"LV [{self.name}] -> {self.path}.log\n"
        fmt += f"Level: {self.level.name}, cout: {self.cout}, fout: {self.fout}\n"
        fmt += f"Overwrite: {self.overwrite}"
        return fmt
        
    def Init(self, name = None, file = None, level = None, cout = None, fout = None, overwrite = None):
        self.Name(name)
        self.File(file)
        self.Level(level)
        self.Cout(cout)
        self.Fout(fout)
        self.Overwrite(overwrite)

    def Name(self, name: str):
        if name is None:
            return
        if not isinstance(name, str):
            raise Exception()
        self.name = name

    def File(self, file: str):
        if file is None:
            return
        if not isinstance(file, str):
            raise Exception()
        self.file = file

    def Level(self, level: Level):
        if level is None:
            return
        if isinstance(level, str):
            level = self.LevelFromStr(level)
        if not isinstance(level, Level):
            raise Exception()
        self.level = level

    def Cout(self, cout: bool):
        if cout is None:
            return
        if not isinstance(cout, bool):
            raise Exception()
        self.cout = cout

    def Fout(self, fout: bool):
        if fout is None:
            return
        if not isinstance(fout, bool):
            raise Exception()
        self.fout = fout

    def Path(self, path):
        if path is None:
            return
        if not isinstance(path, str):
            raise Exception()
        self._path = path

    def Overwrite(self, overwrite: bool):
        if overwrite is None:
            return
        if not isinstance(overwrite, bool):
            raise Exception()
        self.overwrite = overwrite

    def LevelFromStr(self, level: str):
        level = level.upper()
        for lvl in Level:
            if level == lvl.name:
                return lvl
        return None
    
    @property
    def path(self):
        return f"{self._path}/{self.file}"
    
    def Copy(self):
        lv = LoggingVars(self.name, self.file, self.level, self.cout, self.fout, self.overwrite)
        lv.Path(self._path)
        return lv
    
    def Child(self, name: str):
        lv = self.Copy()
        lv.Name(f"{self.name}.{name}")
        lv.File(f"{self.file}/{name}")
        return lv
    
    def Sibling(self, name: str):
        lv = self.Copy()
        lv.Name(f"{'.'.join(self.name.split('.')[:-1])}.{name}")
        lv.File(f"{'/'.join(self.file.split('/')[:-1])}/{name}")
        return lv
    
class Logging:
    def __init__(self, lv: LoggingVars):
        self.lv = lv

        for lvl in Level:
            setattr(self, lvl.name.lower(), lambda msg,self=self,lvl=lvl: self._log(lvl, msg))

    def _header(self, lvl):
        return f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} <{self.lv.name}> {lvl.name}"

    def _log(self, level: Level, msg: str):
        #print(f"{level} >= {self.lv.level} = {level >= self.lv.level}")
        #print(str(self.lv))
        if self.lv.cout and level >= self.lv.level:
            print(f"{self._header(level)}: {msg}")
        if self.lv.fout and self.lv.file is not None:
            try:
                with open(f"{self.lv.path}.log", "a") as f:
                    f.write(f"{self._header(level)}: {msg}\n")
            except FileNotFoundError:
                makedirs(f"{'/'.join(self.lv.path.split('/')[:-1])}")
                with open(f"{self.lv.path}.log", "w") as f:
                    f.write(f"{self._header}: {msg}\n")
