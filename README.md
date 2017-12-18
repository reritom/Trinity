# Trinity

Trinity is a Python based mesh network simulator with a Django HTML/CSS GUI. The purpose of this project is to let you develop routing algorithms for broadcast mesh networks.

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

```
Clone the repository
```
If you have installed Django:
```
Navigate to Trinity/Trinity (there should be a manage.py file in this directory)
```
```
Run the following command in the command line:
python manage.py runserver
```
```
In your browser navigate to 127.0.0.1:8000 (localhost) to use the web interface
```
From the command line:
```
Navigate to Trinity/Trinity/mesh/meshcore (This is where the mesh code is)
```
```
The file propagate.py has some network creation and packet injection examples.
In the file, under "if __name__=='__main__', comment/uncomment the example you want to use and then run:
python propagate.py
```

## Terminology and basic introduction

This section will introduce the main classes and principles of the mesh simulator.
A mesh network consists of multiple nodes or relays. A device is able to interact with a relay to send packets throughout the network of relays to a desired destination. This project allows you to develop your own types of packets, and your own routing rules. The routing rules are what the relays use to determine how to handle the packet, what changes need to be made to the packet, and where to route it to.

# Spark

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

# Cortex

The Cortex is the name for the class which simulates the channels. This class is used to create a graph which creates relay objects, links them, and handles the buffer which simulates the routing of the sparks.

```
PUT HERE AN EXAMPLE OF INSTANTIATING, ADDING RELAYS
```

# Relay

The relay receives the spark from the cortex, decodes it, and then determines how to route it, while also taking relevent data and adding it the relays local network mapping. It then returns a message to the cortex for tracing, and either a None or a spark, if there is something to be routed.

When initialised, the relay isn't aware of any of its surrounding relays. To find them, it either has to receive a Ting from them all, or broadcast a Ping and receive and Pong from each of them.

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
```
- Create a cortex
- Add the relays
- Add some sensors (Optional)
- Inject a packet
- Then:
-   Compare the expected local maps of the relays with what you expect
-   Or check whether a packet has reached the desired destination
-   Or check whether a sensor in the network has been detected
```

## Authors

* **Tomas Sheers** - *Initial work* - [reritom](https://github.com/reritom)
