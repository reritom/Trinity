try:
    from relay import Relay
    from spark import Spark
    from tracer import Tracer
except:
    from meshcore.tracer import Tracer
    from meshcore.relay import Relay
    from meshcore.spark import Spark

import copy
from collections import OrderedDict

class Cortex(Tracer):
    '''
        This class encapsulates an internal mesh network
        made up of relays that can route packets/sparks
    '''

    def __init__(self, debug=True, console=True):
        Tracer.__init__(self)
        self.console = console
        self.debug = debug
        self.logs = OrderedDict()
        self.log_count = 0

        self.relays = dict()
        self.graph = dict()
        self.buffer = list()

    def add_relay(self, name, neighbours):
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
            self.trace_debug("Relay " + name + " not in graph, adding now ")
        else:
            # Add all the neighbours to this relays graph, which haven't already been added
            self.trace_debug("Relay " + name + " IS in graph")
            for neighbour in neighbours:
                if str(neighbour) not in self.graph[name]:
                    self.trace_debug("Relay " + name + " IS in graph, neighbour " + str(neighbour) + " is being added to this relays graph")
                    self.graph[name].append(str(neighbour))

        # Add to relays
        if name not in self.relays:
            self.trace_debug("Relay " + name + " not in relays, adding it now")
            self.relays[name] = Relay(name=name)

        # Add neighbours to graph, with this name as a neighbour
        for neighbour in neighbours:
            if str(neighbour) not in self.graph:
                self.trace_debug("Relay " + name + " neighbour " + str(neighbour) + " not in graph, adding now ")
                self.graph[str(neighbour)] = list()
                self.graph[str(neighbour)].append(name)
            else:
                # Neighbour is in graph, now make sure this relay is in that neighbours graph
                if name not in self.graph[str(neighbour)]:
                    self.trace_debug("Relay " + name + " not in " + str(neighbour) + "'s graph, adding now ")
                    self.graph[str(neighbour)].append(name)

        # Add neighbours to relays
        for neighbour in neighbours:
            if str(neighbour) not in self.relays:
                self.trace_debug("Relay " + name + " neighbour " + str(neighbour) + " not in self.relays, adding now ")
                self.relays[str(neighbour)] = Relay(name=str(neighbour))

        self.trace_line_debug()

    def bridge_graph(self, graph, bridge_link, existing_link):
        pass

    @Tracer.header_style
    def view_cortex(self):
        '''
            This method shows the graph of the cortex
        '''

        print('<--- Cortex Graph --->')

        for key, value in sorted(self.graph.items()):
            self.trace_info(str(key) + ': ' + ','.join(str(e) for e in value))

    def get_relays(self):
        '''
            This method returns the relays
        '''

        return self.relays

    def get_cortex(self):
        '''
            This method returns the graph of the cortex
        '''

        return self.graph


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


    @Tracer.header_style
    def route_buffer(self):
        '''
            The buffer contains all the sparks that need to be sent to relays.
            This method handles the routing of all these sparks
        '''

        while len(self.buffer) > 0:
            # Get the first element in the buffer
            top_spark_in_buffer = self.buffer.pop(0)

            # Pass the spark to the destination relay
            result_spark, result_log = self.relays[top_spark_in_buffer[0]].receive_spark(dict(top_spark_in_buffer[1]))

            # Trace the spark
            result_trace = self.spark_log_gen(result_log)
            self.trace_spark(result_trace)

            # Add the this log to the main logs
            self.log_count += 1
            result_log['Type'] = 'Spark'
            self.logs[self.log_count] = result_log

            # Simulate broadcast, adding receiving relays to the buffer
            if result_spark is not None:
                for destination_of_result in self.graph[result_spark['header']['origin']]:
                    self.buffer.append((destination_of_result, result_spark))

            self.trace_line()

    def show_local(self):
        '''
            This method shows the local mapping for each relay, as inferred from pinging
        '''
        for relay in self.relays:
            self.trace_info(self.relays[relay].name + ":" +  ','.join(str(e) for e in self.relays[relay].locals))
        self.trace_line()

    def show_relay_stats(self):
        '''
            This method shows the stats after session
        '''
        total_received = 0
        total_broadcast = 0

        for relay in self.relays:
            total_received += self.relays[relay].packets_received
            total_broadcast += self.relays[relay].number_of_broadcasts

        self.trace_stat("Total packets received: " + str(total_received) + ", Total broadcasts: " + str(total_broadcast))

    def compare_mappings(self):
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

        self.trace_stat(str(percent) + "% of relays have full local networks mapped")
        self.trace_stat(str(other_percent) + "% of the network has been locally mapped")

    def spark_log_gen(self, log):
        '''
            This receives a spark log dict and creates a (str) message from it for the tracer
        '''
        msg = log['mode'] + " from " + log['origin'] + " aimed at " + log['destination'] + " has arrived at " + log['arrival']
        msg += "\n    " + log['status']
        return msg

    def get_logs(self):
        '''
            This method returns the orderdict containing all the logs
        '''

        return self.logs
