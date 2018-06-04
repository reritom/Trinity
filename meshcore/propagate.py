from cortex import Cortex
from relay import Relay
from spark import Spark

def propagate(console):
    '''
        This method creates a cortex and adds some relay mappings
        :param console: Used by the cortex to control console logging
    '''
    core = Cortex(debug=True, console=console)

    core.add_relay(1, [2,3,4,5])
    core.add_relay(2, [3,4])
    core.add_relay(3, [4,5,13])
    core.add_relay(4, [7,8,9])
    core.add_relay(9, [10])
    core.add_relay(10, [11,12])

    return core

def x_create_spark():
    '''
        Example - Create a ping spark from relay 1
    '''
    spark = Spark(origin=1, destination=None, mode='ping')

    # Add two actions to the message
    spark.add_action("RUN")
    spark.add_action("RESTART")

    # Show the spark
    spark.show_spark()

    # Encode the spark and show the result
    spark.encode_spark()
    this_spark = spark.get_spark()
    print(this_spark)


def x_inject_ping(console=True):
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    # Create a spark
    spark = Spark(origin=1, destination=None, mode='ping')
    spark.encode_spark()
    this_spark = spark.get_spark()

    print(this_spark)
    print("\n")

    # Inject spark in to the cortex
    core.inject(this_spark)
    core.route_buffer()

    core.show_local()
    core.show_relay_stats()

def x_ping_one(console=True):
    '''
        Example - Automatic ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    core.create_ping(4)

    # Process the packets
    core.route_buffer()

    # Show the resulks
    core.show_local()
    core.show_relay_stats()
    core.compare_mapping()

def x_ping_all(console=True):
    '''
        Example - Have all the relays send a ping
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ping packets for each of the relays
    core.ping_all()

    # Process the packets
    core.route_buffer()

    # Show the results
    core.show_local()
    core.show_relay_stats()
    core.compare_mappings()

    return core.get_logs()

def x_inject_explorer(console=True):
    '''
        Example - Manual ping injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    # Create a spark
    spark = Spark(origin=1, destination=None, mode='explorer')
    spark.encode_spark()
    this_spark = spark.get_spark()

    print(this_spark)
    print("\n")

    # Inject spark in to the cortex
    core.inject(this_spark)
    core.route_buffer()

    #core.showLocal()
    core.show_relay_stats()

def x_ting_one(console=True):
    '''
        Example - Automatic ting injection
    '''
    # Create and propagate cortex of relays
    core = propagate(console)

    core.create_ting(2)

    # Process the packets
    core.route_buffer()

    # Show the resulks
    #core.showLocal()
    core.show_relay_stats()
    core.compare_mappings()

def x_ting_all(console=True):
    '''
        Example - Have all the relays send a ting
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ting packets for each of the relays
    core.ting_all()

    # Process the packets
    core.route_buffer()

    # Show the resulks
    core.show_local()
    core.show_relay_stats()
    core.compare_mappings()

def x_complex(console=True):
    '''
        Example - complex
    '''
    # Create and propagate a cortex of relays
    core = propagate(console)

    # Inject ting packet
    core.create_ting(1)

    # Inject a ping packet
    core.create_ping(12)

    # Create an explorer spark
    spark = Spark(origin=1, destination=None, mode='explorer')
    spark.encode_spark()
    this_spark = spark.get_spark()

    core.inject(this_spark)

    core.route_buffer()

    core.show_relay_stats()
    core.compare_mappings()


if __name__ == '__main__':
    print("\n<--- Start --->\n")

    x_ping_all(console=True)
    #x_inject_ping()
    #x_ping_one()
    #x_create_spark()
    #x_inject_explorer()
    #x_ting_one()
    #x_ting_all()
    #x_complex()
    #propagate()

    print("\n<--- End --->\n")
