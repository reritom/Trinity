import random, string

class Spark(object):
    def __init__(self, origin=None, destination=None, mode=None):

        self.message = list()
        self.encoded = False

        self.header = {'origin': str(origin),
                       'destination': str(destination),
                       'mode': mode,
                       'id': self.getID()}

        self.trace = list()
        if origin is not None: self.trace.append(origin)

        self.modes = ['explorer',   # Used for outward network mapping
                      'atlas',      # Used for return mapping
                      'emissary',   # Used for sending actions
                      'ping',       # Used for finding neighbours outward
                      'pong',       # Used for finding neighbours return
                      'ting']       # Used for broadcast in relay presence 

    def getID(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def setMode(self, mode):
        '''
            This method sets the mode, which defines the behaviour of the spark.
        '''
        if mode in self.modes:
            self.header['mode'] = mode
            return True
        else:
            print('invalid mode set')
            return False

    def getMode(self):
        '''
            This method retrieves the mode.
        '''
        return self.header['mode']

    def validateMode(self):

        if self.header['mode'] in self.modes:
            return True
        else:
            print('invalid mode in validation')
            return False

    def setOrigin(self, origin):
        '''
            This method sets the origin.
        '''
        if self.encoded: return False
        self.header['origin'] = str(origin)

        # Add the inital origin as trace, if origin has been changed, change the initial trace value
        if self.trace is None:
            self.trace.append(origin)
        else:
            self.trace[0] = origin

        return self.header['origin']

    def getOrigin(self):
        '''
            This method retrieves the origin.
        '''
        return self.header['origin']

    def setDestination(self, destination):
        '''
            This method sets the destination.
        '''
        if self.encoded: return False
        self.header['destination'] = str(destination)
        return self.header['destination']

    def getDestination(self):
        '''
            This method retrieves the destination.
        '''
        return self.header['destination']

    def validateHeader(self):
        '''
            This method validates that the origin, destination, and mode are set.
        '''
        if self.header['origin'] is None: return False

        if self.validateMode() is False: return False

        if self.header['mode'] == 'ping':
            self.header['destination'] = str(None)
        else:
            if self.header['destination'] is None: return False

        return True

    def validateMessage(self):
        '''
            This method checks that there is at least one action in the message.
        '''
        if self.message is not None or self.header['mode'] == 'ping' or self.header['mode'] == 'pong':
            return True
        else:
            print('invalid message')
            return False

    def encodeSpark(self):
        '''
            This method validates the spark and encodes it.
        '''
        if self.encoded:
            print('already encoded')
            return False

        #validate
        if not self.validateHeader():
            print('invalid header')
            return False

        if not self.validateMessage():
            print('invalid message')
            return False
        #encode header+message
        #set encoded as true
        self.encoded = True
        pass

    def getMessage(self):
        '''
            List of lists, internal lists are actions
        '''
        return self.message

    def addAction(self, action):
        '''
            This method validates the action and appends it to the message.
        '''
        if self.encoded:
            print('cant add action, already encoded')
            return False
        #validate action
        #append action
        self.message.append(action)
        return True

    def addTrace(self, relay_name):
        if self.encoded:
            print('cant add trace, already encoded')
            return False

        self.trace.append(relay_name)

    def getTrace(self):
        return self.trace

    def showSpark(self):
        '''
            This method shows the currently spark.
        '''
        print("\n")
        print("<--- Header --->")
        for key, value in self.header.items():
            print(key + ': ' + str(value))

        print("<--- Trace --->")
        for address in self.trace:
            print("address: " + str(address))

        print('<--- Message --->')
        if not self.message:
            print("No actions")
        else:
            for action in self.message:
                print(action)
        print("\n")

    def getSpark(self):
        if not self.encoded:
            print('cant get spark, not encoded')
            return False

        this_spark = dict()
        this_spark['header'] = self.header
        this_spark['trace'] = self.trace
        this_spark['message'] = self.message

        return this_spark
