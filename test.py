import qvlog

def Logger():
    log = qvlog.Logger.Get("testLogger", None, qvlog.Level.TRACE, True, True)
    log.debug("Hello world!")
    log.Child("child")
    log.child.info("Hi!")
    log.child.Sibling("sibling")
    log.child.sibling.warn("Ahhhhh!")

def ConsoleLogger():
    log = qvlog.ConsoleLogger.Get("console")

def SocketLogger():
    log = qvlog.SocketLogger.Get("socket", None, qvlog.Level.TRACE, True, True)
    log.info("Hello world!")

if __name__ == '__main__':
    SocketLogger()