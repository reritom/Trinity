from cortex import Cortex
from spark import Spark

def propagate():
    '''
        This method creates a cortex and adds some relay mappings
    '''
    core = Cortex()

    core.addRelay(1, [2,3,4,5])
    core.addRelay(2, [1,3,4])
    core.addRelay(3, [1,2,4,5])
    core.addRelay(4, [1,2,3,7,8,9])
    core.addRelay(5, [1,3])
    core.addRelay(7, [4])
    core.addRelay(8, [4])
    core.addRelay(9, [4,10])
    core.addRelay(10, [9,11,12])
    core.addRelay(11, [10])
    core.addRelay(12, [10])

    #core.viewCortex()
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


def xInjectPing():
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate()

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

def xPingOne():
    '''
        Example - Automatic ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate()

    core.createPing(4)

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xPingAll():
    '''
        Example - Have all the relays send a ping
    '''
    # Create and propagate a cortex of relays
    core = propagate()

    # Inject ping packets for each of the relays
    core.pingAll()

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    #core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xInjectExplorer():
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate()

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

def xTingOne(val):
    '''
        Example - Automatic ting injection
    '''
    # Create and propagate cortex of relays
    core = propagate()

    core.createTing(val)

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    #core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xTingAll():
    '''
        Example - Have all the relays send a ting
    '''
    # Create and propagate a cortex of relays
    core = propagate()

    # Inject ting packets for each of the relays
    core.tingAll()

    # Process the packets
    core.routeBuffer()

    # Show the resulks
    #core.showLocal()
    core.showRelayStats()
    core.compareMapping()

def xComplex():
    '''
        Example - complex
    '''
    # Create and propagate a cortex of relays
    core = propagate()

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


if __name__ == '__main__':
    print("\n<--- Start --->\n")

    #xPingAll()
    #xInjectPing()
    #xPingOne()
    #xCreateSpark()
    #xInjectExplorer()
    #xTingOne(2)
    #xTingAll()
    xComplex()

    print("\n<--- End --->\n")
