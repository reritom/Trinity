import os

class Tracer(object):
    def __init__(self):
        self.debug = True
        self.console = True

        self.col = {'INFO':'\033[1;36;40m',
                    'DEBUG':'\033[1;35;40m',
                    'WARNING':'\033[1;33;40m',
                    'ERROR':'\033[1;31;40m',
                    'NORMAL':'\033[1;37;40m',
                    'STAT':'\033[1;34m',
                    'SPARK':'\033[1;32m'}

        # This colour tagging only works in unix/posix

        if os.name != "posix":
            for col in self.col:
                self.col[col] = ""


    def debug_on(self):
        '''
            Set the debug to True
        '''

        self.debug = True

    def debug_off(self):
        '''
            Set the debug to False
        '''

        self.debug = False

    def console_on(self):
        '''
            Turn on console logs
        '''

        self.console = True

    def console_off(self):
        '''
            Turn off console logs
        '''

        self.console = False

    def trace_info(self, message):
        if self.validate_message(message):
            print("[" + self.col['INFO'] + "INFO" + self.col['NORMAL'] + "] " + message)

    def trace_error(self, message):
        if self.validate_message(message):
            print("[" + self.col['ERROR'] + "ERROR" + self.col['NORMAL'] + "] " + message)

    def trace_warning(self, message):
        if self.validate_message(message):
            print("[" + self.col['WARNING'] + "WARNING" + self.col['NORMAL'] + "] " + message)

    def trace_debug(self, message):
        if self.validate_message(message) and self.debug:
            print("[" + self.col['DEBUG'] + "DEBUG" + self.col['NORMAL'] + "] " + message)

    def trace_line(self):
        if self.console:
            print("\n")

    def trace_line_debug(self):
        if self.debug:
            print("\n")

    def trace_stat(self, message):
        if self.validate_message(message):
            print("[" + self.col['STAT'] + "STAT" + self.col['NORMAL'] + "] " + message)

    def trace_spark(self, message):
        if self.validate_message(message):
            print("[" + self.col['SPARK'] + "SPARK" + self.col['NORMAL'] + "] " + message)

    def validate_message(self, message):
        '''
            Check that the tracer message is a string.
        '''

        if not isinstance(message, str):
            return self.trace_error("Message needs to be string for tracer")
        elif self.console is False:
            return False
        else:
            return True

    @staticmethod
    def header_style(viewFunction):
        '''
            This method take a function designed for viewing data, and prints
            a wrapper for it.
        '''

        def wrapper(*args):
            this = args[0]
            this.trace_warning("Start of " + viewFunction.__name__)
            viewFunction(*args)
            this.trace_warning("End of " + viewFunction.__name__)
            return True
        return wrapper
