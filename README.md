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

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
