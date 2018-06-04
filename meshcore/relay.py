try:
    from spark import Spark
except:
    from meshcore.spark import Spark

import copy

class Relay(object):
    def __init__(self, name):
        self.name = name
        self.neighbours = list()
        self.locals = set()
        self.packets_received = 0
        self.number_of_broadcasts = 0
        self.id_buffer = dict() # Key is message ID, value is timestamp, daemon clears this up.

    def receive_spark(self, spark):
        '''
            This method receives a spark from the cortex, calls the decoder and subsequent routing,
            and then returns the modified spark to the cortex
        '''
        # Received from the Cortex

        self.packets_received += 1

        routed_spark = self.decode_spark(spark)

        if routed_spark[0] is not None:
            self.number_of_broadcasts += 1

        return routed_spark

    def decode_spark(self, spark):
        '''
            In practice, the spark will be encoded and need decoding before routing (only the header needs decoding).
            Here, the decoded spark is basically the actual spark.
        '''
        decoded_spark = spark

        return self.route_spark(decoded_spark)

    def route_spark(self, spark):
        '''
            This method modifies the spark for routing purposes based on the contents of it.
        '''

        log = {'mode': spark['header']['mode'],
               'origin': spark['header']['origin'],
               'destination': spark['header']['destination'],
               'arrival': self.name}

        '''
        this_trace = copy.deepcopy(spark['trace'])
        this_trace[::-1]

        for relay in this_trace:
            pass
        '''

        # A pong for this relay is accepted into the mapping. IDs need to be compared and removed from the idbuffer

        if spark['header']['destination'] == self.name and spark['header']['mode'] == 'pong':
            self.locals.add(spark['header']['origin'])
            log['status'] = "This packet has been accepted as a pong directed at this relay"
            return None, log

        # Tings and Pongs get accepted to modify local map, but not forwarded or stored.

        if spark['header']['mode'] == 'pong':
            self.locals.add(spark['header']['origin'])
            log['status'] = "This packet has been accepted as an indirect pong"
            return None, log

        if spark['header']['mode'] == 'ting':
            self.locals.add(spark['header']['origin'])
            log['status'] = "This packet has been accepted as a ting"
            return None, log

        # Pings get rerouted as pongs

        if spark['header']['mode'] == 'ping':
            pong = copy.deepcopy(spark)
            pong['header']['mode'] = 'pong'
            pong['header']['origin'] = self.name
            pong['header']['destination'] = spark['header']['origin']
            pong['trace'].append(self.name)

            log['status'] = "This packet has been accepted as a ping and forwarded as a pong"
            return pong, log

        log['status'] = "This packet has been ignored"
        return None, log
