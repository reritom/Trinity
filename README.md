# Trinity

Trinity is a Python based mesh network simulator with a Django HTML/CSS GUI. The purpose of this project is to let you develop routing algorithms for broadcast mesh networks.

### Note: This is still in development. The Django GUI hasn't been made, and routing algorithms are still being developed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

The mesh simulator can be run directly from the command line without using the Django interface.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.5+
Django v1.11.1 (for GUI, not required for cmd-line usage)
```

### Installing

A step by step series of examples that tell you have to get a development env running

- Clone the repository

If you have installed Django:

- Navigate to Trinity/Trinity (there should be a manage.py file in this directory)
- Run the following command in the command line:
```
python manage.py runserver
```

- In your browser navigate to 127.0.0.1:8000 (localhost) to use the web interface

From the command line:
- Navigate to Trinity/Trinity/mesh/meshcore (This is where the mesh code is)

The file propagate.py has some network creation and packet injection examples.
In the file, under "if __name__=='__main__'", comment/uncomment the example you want to use and then run:
```
python propagate.py
```

## Terminology and basic introduction

This section will introduce the main classes and principles of the mesh simulator.
A mesh network consists of multiple nodes or relays. A device is able to interact with a relay to send packets throughout the network of relays to a desired destination. This project allows you to develop your own types of packets, and your own routing rules. The routing rules are what the relays use to determine how to handle the packet, what changes need to be made to the packet, and where to route it to.

### Spark

The spark is the name for the packet used in this system. For the simplictiy, it is a JSON object of the following format

```
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
```

A spark can be one of multiple modes which have different purposes.

    ping - An outward packet sent from a relay. If a ping is received, the only response is a pong. This allows a relay to map
           its local network.
           
    pong - if a ping is received, a pong is sent, with its destination set as the origin of the ping.
    
    ting - a relay broadcasting its presence, but expecting no reply.
    
    explorer - An explorer is sent by a relay to map an entire network
    
    atlas - explorers trigger the release of atlas packets, which return from different points in the network to the origin
    
    emmisary - this carries an action message from an origin to a known destination. Such as sending a data request

The spark class is used to create a spark, the following example creates a spark with the origin being a relay named '1', and no set destination, with the ping mode, and two actions (though pings wouldn't carry actions in practise):

```
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
```

### Cortex

The Cortex is the name for the class which simulates the channels. This class is used to create a graph which creates relay objects, links them, and handles the buffer which simulates the routing of the sparks.

The following example creates a cortex, and adds some relays into the graph. With debug set to True, there are a lot more logs of what is happening in the cortex.

```
core = Cortex(debug=False)

core.addRelay(1, [2,3,4,5])
core.addRelay(2, [3,4])
core.addRelay(3, [4,5,13])
core.addRelay(4, [7,8,9])
core.addRelay(9, [10])
core.addRelay(10, [11,12])
```

Currently, the relay connections are assumed to be bi-directional. Therefore, for following snippet creates two relays with bi-directional communication implicitly.

```
core = Cortex(debug=False)

core.addRelay(1, [2])
# core.addRelay(2, [1]) # This line is not needed
```

### Relay

The relay receives the spark from the cortex, decodes it, and then determines how to route it, while also taking relevent data and adding it the relays local network mapping. It then returns a message to the cortex for tracing, and either a None or a spark, if there is something to be routed.

When initialised, the relay isn't aware of any of its surrounding relays. To find them, it either has to receive a Ting from them all, or broadcast a Ping and receive and Pong from each of them.

## Examples

### Inject Ting Packets for all relays

The following example creates a cortex, adds some relays, and then injects a Ting from each of the relays (This would allow all of the relays to become aware of all of their neighbouring relays.

```
def propagate():
    '''
        This method creates a cortex and adds some relay mappings
    '''
    core = Cortex(debug=False)

    core.addRelay(1, [2,3,4,5])
    core.addRelay(2, [3,4])
    core.addRelay(3, [4,5,13])
    core.addRelay(4, [7,8,9])
    core.addRelay(9, [10])
    core.addRelay(10, [11,12])

    return core
    
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
    core.showLocal()
    core.showRelayStats()
    core.compareMapping()
    
if __name__ == '__main__':
    xTingAll()
```

### Create a single packet and inject it

```
def propagate():
    '''
        This method creates a cortex and adds some relay mappings
    '''
    core = Cortex(debug=False)

    core.addRelay(1, [2,3,4,5])
    core.addRelay(2, [3,4])
    core.addRelay(3, [4,5,13])
    core.addRelay(4, [7,8,9])
    core.addRelay(9, [10])
    core.addRelay(10, [11,12])

    return core
    
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

    # Inject spark in to the cortex
    core.inject(this_spark)
    core.routeBuffer()

    # Results
    core.showLocal()
    core.showRelayStats()
    
if __name__ == '__main__':
    xInjectExplorer()
```

### Small Example with walkthrough

```
TODO - Create 3 relay cortex, inject packet, explain where it goes and whats happening
```


## Running the tests

This system has tests for the mesh simulation aspect. But will need to be adjusted/rewritten depending on what routing algorithms you implement.

### Break down of mesh tests

The tests can be found in Trinity/Trinity/mesh/meshcore/tests/tests.py
To add a new test, follow the following title and docstring format:

```
def testTestname():
  '''
      Test - Information about the test goes here..
  '''
```

Tests can either be run directly or they can all be run using the following command in the tests directory:

```
python runTests.py
```

When creating your own test, the general format is:

- Create a cortex
- Add the relays
- Add some sensors (Optional)
- Inject a packet
- Then:
-   Compare the expected local maps of the relays with what you expect
-   Or check whether a packet has reached the desired destination
-   Or check whether a sensor in the network has been detected


## Things to do

- The cortex needs to be able to handle different channels with different rules, for example, to simulate a network which uses both RF and Bluetooth to connect relays.
- Relative distances between relays should be added, so that the order that packets are received can be simulated.
- [P] Django GUI needs finishing
- Basic routing protocols should be applied and documented.
- Sensors should be added, to simulate devices interacting with the network
- Add a spark (Pilgrim) which is destined for all relays, to searching for relays in the network which have connected devices. Similar behaviour to an Explorer
- Create an example function which propagates the local mappings of relays so that routing can be tested more easily.
- Add an application layer to the sensor which allows for message encryption (#FeatureDrift)
- For implementing routing (https://pdfs.semanticscholar.org/379d/087b54850fa6d98c07c2e3bb66f51a109179.pdf)
- When running multiple injections, add tags to the logs of each section so that logs can be sorted in Django better.
- [P] Create a graph generator. Allow for 1 to n-1 neighbours. Allow the topology to change during the simulation.
- Make a packet for naming a relay and linking a sensor name to a relay.
- Make a packet which checks the relay name doesn't exist in the local network already.
- Add ability to turn on/off relays and add/rename relays mid simulation
- Add events at the beginning which get processed in the routeBuffer at specified times, such as topology changes, etc.

Tags -> [P] in progress, [X] completed

## Authors

* **Tomas Sheers** - *Initial work* - [reritom](https://github.com/reritom)
