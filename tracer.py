class Tracer(object):
    def __init__(self):
        self.debug = True

        self.col = {'INFO':'\033[1;36;40m',
                    'DEBUG':'\033[1;35;40m',
                    'WARNING':'\033[1;33;40m',
                    'ERROR':'\033[1;31;40m',
                    'NORMAL':'\033[1;37;40m',
                    'STAT':'\033[1;34m',
                    'SPARK':'\033[1;32m'}

    def debugOn(self):
        '''
            Set the debug to True
        '''

        self.debug = True

    def debugOff(self):
        '''
            Set the debug to False
        '''

        self.debug = False

    def traceInfo(self, message):
        if self.validateMessage(message):
            print("[" + self.col['INFO'] + "INFO" + self.col['NORMAL'] + "] " + message)

    def traceError(self, message):
        if self.validateMessage(message):
            print("[" + self.col['ERROR'] + "ERROR" + self.col['NORMAL'] + "] " + message)

    def traceWarning(self, message):
        if self.validateMessage(message):
            print("[" + self.col['WARNING'] + "WARNING" + self.col['NORMAL'] + "] " + message)

    def traceDebug(self, message):
        if self.validateMessage(message) and self.debug:
            print("[" + self.col['DEBUG'] + "DEBUG" + self.col['NORMAL'] + "] " + message)

    def traceLine(self):
        print("\n")

    def traceLineDB(self):
        if self.debug:
            print("\n")

    def traceStat(self, message):
        if self.validateMessage(message):
            print("[" + self.col['STAT'] + "STAT" + self.col['NORMAL'] + "] " + message)

    def traceSpark(self, message):
        if self.validateMessage(message):
            print("[" + self.col['SPARK'] + "SPARK" + self.col['NORMAL'] + "] " + message)

    def validateMessage(self, message):
        '''
            Check that the tracer message is a string.
        '''

        if not isinstance(message, str):
            return self.traceError("Message needs to be string for tracer")
        else:
            return True

    @staticmethod
    def headerStyle(viewFunction):
        '''
            This method take a function designed for viewing data, and prints
            a wrapper for it.
        '''

        def wrapper(*args):
            this = args[0]
            this.traceWarning("Start of " + viewFunction.__name__)
            viewFunction(*args)
            this.traceWarning("End of " + viewFunction.__name__)
            return True
        return wrapper
