'''
    How to implement OTA updates of relay routing and internal information (relay name, etc)?

    SPARK-TYPES:

    ping - An outward packet sent from a relay. If a ping is received, the only response is a pong. This allows a relay to map
           its local network.

    pong - if a ping is received, a pong is sent, with its destination set as the origin of the ping.

    ting - a relay broadcasting its presence, but expecting no reply.

    explorer - An explorer is sent by a relay to map an entire network

    atlas - explorers trigger the release of atlas packets, which return from different points in the network to the origin

    emmisary - this carries an action message from an origin to a known destination. Such as sending a data request

    TO-DO:

    - implementation of different channels types to simulate overlapping BT, RF, SR networks

    CLASSES:

    cortex - This creates a network of relays. Sparks can be sent to a relay, and the output of the relay is then
             sent to the relevent surrounding relays. The cortex simulates the channels connecting the relays

    relay - a relay receives a spark, decodes it, and determines how to route it, before returning the modified spark to the cortex.

    spark - a spark is a packet of the following format:

        {
            "header": {
                            "origin" (str) : The name of the origin relay
                            "destination" (str) : The destination relay. "None" if it is a ping or explorer
                            "mode" (str) : This is the type of spark.
                            "id" (str) : This is an identifier for the spark (needs defining)
                      }
            "trace":  [
                            (str) List of relay names that the spark has been routed through, starting from the origin
                      ]

            "message":[
                            (str) List of messages in a defined format
                      ]
        }
'''

#TODO - In local mapping, look at the trace of incoming packets and add to local map

'''
    Set destination as an attribute of the sensor you want to message. Or allow explorers to send messages.. Or create new type, pilgrim, which have their messages
    by all the relays, which is slower, but allows for multiple destinations.

    allow for encrypted messages/relays

    if a relay has already processed an ID, ignore?

    message received, confirmation emissaries?

    only send pings and not pongs? it'll have the same effect for local mapping.. pingpong-ing can be used for checking something is still active.

'''

'''
    On load, run a pingpong to get local network. Timestamp local responses.
    listen for tings, use them to update timestamps (and all other packets)
    if timestamp is greater than given value, run a pingpong
'''

'''
    Create web view for tracking packets and for maping for the graph and stats
    allow packets to be filtered
    have setup docs on site
    have example processes

    return data from relay before creating msg for tracer
'''

'''
    Create physical system. Add application layer with chat system example
'''
'''
    When timing is implemented, introduce packet loss due to collisions
    add a module that handles declarations of broadcast intent (for collision avoidance)
    
'''
