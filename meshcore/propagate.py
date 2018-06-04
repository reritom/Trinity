try:
    from mesh.meshcore.cortex import Cortex
    from mesh.meshcore.relay import Relay
    from mesh.meshcore.spark import Spark
except:
    from cortex import Cortex
    from relay import Relay
    from spark import Spark

def propagate(console):
    '''
        This method creates a cortex and adds some relay mappings
        :param console: Used by the cortex to control console logging
    '''
    core = Cortex(debug=False, console=console)

    core.addRelay(1, [2,3,4,5])
    core.addRelay(2, [3,4])
    core.addRelay(3, [4,5,13])
    core.addRelay(4, [7,8,9])
    core.addRelay(9, [10])
    core.addRelay(10, [11,12])

    return core

def xCreateSpark():
    '''
        Example - Create a ping spark from relay 1
    '''
    spark = Spark(origin=1, destination=None, mode='ping')

    # Add two actions to the message
    spark.addAction("RUN")
    spark.addAction("RESTART")

    # Show the spark
    spark.showSpark()

    # Encode the spark and show the result
    spark.encodeSpark()
    this_spark = spark.getSpark()
    print(this_spark)


def xInjectPing(console=True):
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    # Create a spark
    spark = Spark(origin=1, destination=None, mode='ping')
    spark.encodeSpark()
    this_spark = spark.getSpark()

    print(this_spark)
    print("\n")

    # Inject spark in to the cortex
    core.inject(this_spark)
    core.routeBuffer()

    core.showLocal()
    core.showRelayStats()

def xPingOne(console=True):
    '''
        Example - Automatic ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    core.createPing(4)

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xPingAll(console=True):
    '''
        Example - Have all the relays send a ping
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ping packets for each of the relays
    core.pingAll()

    # Process the packets
    core.routeBuffer()

    # Show the results
    core.showLocal()
    core.showRelayStats()
    core.compareMapping()

    return core.getLogs()

def xInjectExplorer(console=True):
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    # Create a spark
    spark = Spark(origin=1, destination=None, mode='explorer')
    spark.encodeSpark()
    this_spark = spark.getSpark()

    print(this_spark)
    print("\n")

    # Inject spark in to the cortex
    core.inject(this_spark)
    core.routeBuffer()

    #core.showLocal()
    core.showRelayStats()

def xTingOne(console=True):
    '''
        Example - Automatic ting injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    core.createTing(2)

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    #core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xTingAll(console=True):
    '''
        Example - Have all the relays send a ting
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ting packets for each of the relays
    core.tingAll()

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xComplex(console=True):
    '''
        Example - complex
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ting packet
    core.createTing(1)

    # Inject a ping packet
    core.createPing(12)

    # Create an explorer spark
    spark = Spark(origin=1, destination=None, mode='explorer')
    spark.encodeSpark()
    this_spark = spark.getSpark()

    core.inject(this_spark)

    core.routeBuffer()

    core.showRelayStats()
    core.compareMapping()


if __name__ == '__main__':
    print("\n<--- Start --->\n")

    xPingAll(console=False)
    #xInjectPing()
    #xPingOne()
    #xCreateSpark()
    #xInjectExplorer()
    #xTingOne()
    #xTingAll()
    #xComplex()
    #propagate()

    print("\n<--- End --->\n")
