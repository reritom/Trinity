from relay import Relay
from spark import Spark
import copy

class Cortex(object):
    '''
        This class encapsulates an internal mesh network
    '''
    def __init__(self):
        self.relays = dict()
        self.graph = dict()
        self.buffer = list()

    def addRelay(self, name, neighbours):
        '''
            A relay is used to route the sparks across the network.
            This method creates a new relay.
        '''

        # Input validation
        name = str(name)

        if name is None: return False
        #if not isinstance(channels, list): return False
        if not isinstance(neighbours, list): return False

        # Add to graph

        if name not in self.graph and name not in self.relays:
            self.graph[name] = list()
            self.graph[name].extend(str(neighbour) for neighbour in neighbours)
            self.relays[name] = Relay(name=name)
            return True
        else:
            return False

    def viewCortex(self):
        '''
            This method shows the graph of the cortex
        '''
        print('<--- Cortex --->')
        for key, value in self.graph.items():
            print(str(key) + ': ' + ','.join(str(e) for e in value))

    def getRelays(self):
        '''
            This method returns the relays
        '''
        return self.relays

    def getCortex(self):
        '''
            This method returns the graph of the cortex
        '''
        return self.graph

    def pingAll(self):
        '''
            This method injects a ping packet from each of the relays.
        '''

        for relay in self.relays:
            # Create a spark
            spark = Spark(origin=self.relays[relay].name, destination=None, mode='ping')
            spark.encodeSpark()
            this_spark = spark.getSpark()
            self.inject(this_spark)

    def tingAll(self):
        '''
            This method injects a ting packet from each of the relays.
        '''

        for relay in self.relays:
            # Create a spark
            spark = Spark(origin=self.relays[relay].name, destination=None, mode='ting')
            spark.encodeSpark()
            this_spark = spark.getSpark()
            self.inject(this_spark)

    def inject(self, spark):
        '''
            This method injects a spark into the routing buffer
        '''
        # read spark
        # route spark to other relays, add relay requeststo buffer, process buffer until empty.
        injected_relay = spark['header']['origin']

        #find destination relays and append to the buffer with the spark
        for destination_relay in self.graph[injected_relay]:
            self.buffer.append((destination_relay, spark))

        self.relays[injected_relay].number_of_broadcasts += 1

        return True

    def createPing(self, relay_name):
        '''
            For a relay, create a ping
        '''
        spark = Spark(origin=relay_name, destination=None, mode='ping')
        spark.encodeSpark()
        this_spark = spark.getSpark()
        self.inject(this_spark)

    def createTing(self, relay_name):
        '''
            For a relay, create a ping
        '''
        spark = Spark(origin=relay_name, destination=None, mode='ting')
        spark.encodeSpark()
        this_spark = spark.getSpark()
        self.inject(this_spark)

    def routeBuffer(self):
        '''
            The buffer contains all the sparks that need to be sent to relays.
            This method handles the routing of all these sparks
        '''
        #for element in self.buffer:
        #    print(element)
        #print("\n")

        while len(self.buffer) > 0:

            '''
            buflist = list()
            for buf in self.buffer:
                buflist.append(buf[0])
            print("Current Buffer Size: ", len(self.buffer), buflist)
            '''

            #go through the buffer, do stuff
            top_spark_in_buffer = self.buffer.pop(0)

            #pass the spark to the destination relay
            result_spark = self.relays[top_spark_in_buffer[0]].receiveSpark(dict(top_spark_in_buffer[1]))

            if result_spark is not None:
                for destination_of_result in self.graph[result_spark['header']['origin']]:
                    self.buffer.append((destination_of_result, result_spark))

            print("\n")

    def showLocal(self):
        '''
            This method shows the local mapping for each relay, as inferred from pinging
        '''
        for relay in self.relays:
            print(self.relays[relay].name, self.relays[relay].locals)
        print('\n')

    def showRelayStats(self):
        '''
            This method shows the stats after session
        '''
        total_received = 0
        total_broadcast = 0

        for relay in self.relays:
            #print(self.relays[relay].name, " received: ", self.relays[relay].packets_received, " broadcasts: ", self.relays[relay].number_of_broadcasts)
            total_received += self.relays[relay].packets_received
            total_broadcast += self.relays[relay].number_of_broadcasts

        print("Total packets received: " + str(total_received) + ", Total broadcasts: " + str(total_broadcast))

    def compareMapping(self):
        '''
            This map compares the actual network graph, with what the relays can see locally
        '''
        success_counter = 0

        full_count = 0
        full_success = 0

        for relay in self.relays:

            relay_graph = list(self.relays[relay].locals)
            cortex_graph = self.graph[relay]

            relay_graph.sort()
            cortex_graph.sort()

            full_count += len(self.graph[relay])

            for node in self.relays[relay].locals:
                if node in self.graph[relay]:
                    full_success += 1

            #print(relay, "relay", relay_graph)
            #print(relay, "cortex", cortex_graph)

            if relay_graph == cortex_graph:
                success_counter += 1

        percent = float(success_counter)/float(len(self.relays)) * 100

        other_percent = float(full_success) / float(full_count) * 100

        #print("ff: " + str(full_success) + " " + str(full_count))
        #print(full_success/full_count)

        print(str(percent) + "% of relays have full local networks mapped")
        print(str(other_percent) + "% of the network has been locally mapped")
