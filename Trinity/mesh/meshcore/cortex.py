try:
    from mesh.meshcore.relay import Relay
    from mesh.meshcore.spark import Spark
    from mesh.meshcore.tracer import Tracer
except:
    from relay import Relay
    from spark import Spark
    from tracer import Tracer
import copy

class Cortex(Tracer):
    '''
        This class encapsulates an internal mesh network
        made up of relays that can route packets/sparks
    '''

    def __init__(self, debug=True):
        Tracer.__init__(self)
        self.debug = debug

        self.relays = dict()
        self.graph = dict()
        self.buffer = list()

    def addRelay(self, name, neighbours):
        '''
            A relay is used to route the sparks across the network.
            This method creates a new relay and updates the cortex network graph.
        '''

        # Input validation
        name = str(name)

        if name is None: return False
        #if not isinstance(channels, list): return False
        if not isinstance(neighbours, list): return False

        # Add to graph
        if name not in self.graph:
            self.graph[name] = list()
            self.graph[name].extend(str(neighbour) for neighbour in neighbours)
            #self.trace('debug', ("Relay " + name + " not in graph, adding now "))
            self.traceDebug("Relay " + name + " not in graph, adding now ")
        else:
            # Add all the neighbours to this relays graph, which haven't already been added
            self.traceDebug("Relay " + name + " IS in graph")
            for neighbour in neighbours:
                if str(neighbour) not in self.graph[name]:
                    self.traceDebug("Relay " + name + " IS in graph, neighbour " + str(neighbour) + " is being added to this relays graph")
                    self.graph[name].append(str(neighbour))

        # Add to relays
        if name not in self.relays:
            self.traceDebug("Relay " + name + " not in relays, adding it now")
            self.relays[name] = Relay(name=name)

        # Add neighbours to graph, with this name as a neighbour
        for neighbour in neighbours:
            if str(neighbour) not in self.graph:
                self.traceDebug("Relay " + name + " neighbour " + str(neighbour) + " not in graph, adding now ")
                self.graph[str(neighbour)] = list()
                self.graph[str(neighbour)].append(name)
            else:
                # Neighbour is in graph, now make sure this relay is in that neighbours graph
                if name not in self.graph[str(neighbour)]:
                    self.traceDebug("Relay " + name + " not in " + str(neighbour) + "'s graph, adding now ")
                    self.graph[str(neighbour)].append(name)

        # Add neighbours to relays
        for neighbour in neighbours:
            if str(neighbour) not in self.relays:
                self.traceDebug("Relay " + name + " neighbour " + str(neighbour) + " not in self.relays, adding now ")
                self.relays[str(neighbour)] = Relay(name=str(neighbour))

        self.traceLineDB()

    @Tracer.headerStyle
    def viewCortex(self):
        '''
            This method shows the graph of the cortex
        '''

        print('<--- Cortex Graph --->')

        for key, value in sorted(self.graph.items()):
            self.traceInfo(str(key) + ': ' + ','.join(str(e) for e in value))

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

    @Tracer.headerStyle
    def routeBuffer(self):
        '''
            The buffer contains all the sparks that need to be sent to relays.
            This method handles the routing of all these sparks
        '''

        while len(self.buffer) > 0:
            # Get the first element in the buffer
            top_spark_in_buffer = self.buffer.pop(0)

            # Pass the spark to the destination relay
            result_spark, result_trace = self.relays[top_spark_in_buffer[0]].receiveSpark(dict(top_spark_in_buffer[1]))

            self.traceSpark(result_trace)

            if result_spark is not None:
                for destination_of_result in self.graph[result_spark['header']['origin']]:
                    self.buffer.append((destination_of_result, result_spark))

            self.traceLine()

    def showLocal(self):
        '''
            This method shows the local mapping for each relay, as inferred from pinging
        '''
        for relay in self.relays:
            self.traceInfo(self.relays[relay].name + ":" +  ','.join(str(e) for e in self.relays[relay].locals))
        self.traceLine()

    def showRelayStats(self):
        '''
            This method shows the stats after session
        '''
        total_received = 0
        total_broadcast = 0

        for relay in self.relays:
            total_received += self.relays[relay].packets_received
            total_broadcast += self.relays[relay].number_of_broadcasts

        self.traceStat("Total packets received: " + str(total_received) + ", Total broadcasts: " + str(total_broadcast))

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

            if relay_graph == cortex_graph:
                success_counter += 1

        percent = float(success_counter)/float(len(self.relays)) * 100
        other_percent = float(full_success) / float(full_count) * 100

        self.traceStat(str(percent) + "% of relays have full local networks mapped")
        self.traceStat(str(other_percent) + "% of the network has been locally mapped")
