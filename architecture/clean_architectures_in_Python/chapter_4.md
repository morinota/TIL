## link

https://www.thedigitalcatbooks.com/pycabook-chapter-04/

# Chapter 4 - Add a web application

For your information, Hairdo, a major network is interested in me.

Groundhog Day, 1993

In this chapter, I will go through the creation of an HTTP endpoint for the room list use case. An HTTP endpoint is a URL exposed by a Web server that runs a specific logic and returns values in a standard format.

I will follow the REST recommendation, so the endpoint will return a JSON payload. REST is however not part of the clean architecture, which means that you can choose to model your URLs and the format of returned data according to whatever scheme you prefer.

To expose the HTTP endpoint we need a web server written in Python, and in this case, I chose Flask. Flask is a lightweight web server with a modular structure that provides just the parts that the user needs. In particular, we will not use any database/ORM, since we already implemented our own repository layer.

## Flask setup

Let us start updating the requirements files. The file requirements/prod.txt shall mention Flask, as this package contains a script that runs a local webserver that we can use to expose the endpoint

The file requirements/test.txt will contain the pytest extension to work with Flask (more on this later)

Remember to run pip install -r requirements/dev.txt again after those changes to install the new packages in your virtual environment.

The setup of a Flask application is not complex, but there are a lot of concepts involved, and since this is not a tutorial on Flask I will run quickly through these steps. I will provide links to the Flask documentation for every concept, though. If you want to dig a bit deeper in this matter you can read my series of posts Flask Project Setup: TDD, Docker, Postgres and more.

The Flask application can be configured using a plain Python object (documentation), so I created the file application/config.py that contains this code

Read this page to know more about Flask configuration parameters.

Now we need a function that initialises the Flask application (documentation), configures it, and registers the blueprints (documentation). The file application/app.py contains the following code, which is an app factory

## Test and create an HTTP endpoint
Before we create the proper setup of the webserver, we want to create the endpoint that will be exposed. Endpoints are ultimately functions that are run when a user sends a request to a certain URL, so we can still work with TDD, as the final goal is to have code that produces certain results.

The problem we have testing an endpoint is that we need the webserver to be up and running when we hit the test URLs. The webserver itself is an external system so we won't test it, but the code that provides the endpoint is part of our application[1]. It is actually a gateway, that is an interface that allows an HTTP framework to access the use cases.

The extension pytest-flask allows us to run Flask, simulate HTTP requests, and test the HTTP responses. This extension hides a lot of automation, so it might be considered a bit "magic" at a first glance. When you install it some fixtures like client are available automatically, so you don't need to import them. Moreover, it tries to access another fixture named app that you have to define. This is thus the first thing to do.

Fixtures can be defined directly in your test file, but if we want a fixture to be globally available the best place to define it is the file conftest.py which is automatically loaded by pytest. As you can see there is a great deal of automation, and if you are not aware of it you might be surprised by the results, or frustrated by the errors.

The function app runs the app factory to create a Flask app, using the configuration testing, which sets the flag TESTING to True. You can find the description of these flags in the official documentation.

At this point, we can write the test for our endpoint.

Let's comment it section by section.

The first part contains some imports and sets up a room from a dictionary. This way we can later directly compare the content of the initial dictionary with the result of the API endpoint. Remember that the API returns JSON content, and we can easily convert JSON data into simple Python structures, so starting from a dictionary will come in handy.

This is the only test that we have for the time being. During the whole test, we mock the use case, as we are not interested in running it, as it has been already tested elsewhere. We are however interested in checking the arguments passed to the use case, and a mock can provide this information. The test receives the mock from the decorator patch and the fixture client, which is one of the fixtures provided by pytest-flask. The fixture automatically loads app, which we defined in conftest.py, and is an object that simulates an HTTP client that can access the API endpoints and store the responses of the server.

The first line initialises the mock use case, instructing it to return the fixed rooms variable that we created previously. The central part of the test is the line where we get the API endpoint, which sends an HTTP GET request and collects the server's response.

After this, we check that the data contained in the response is a JSON that contains the data in the structure room_dict, that the method use_case has been called, that the HTTP response status code is 200, and last that the server sends the correct MIME type back.

It's time to write the endpoint, where we will finally see all the pieces of the architecture working together, as they did in the little CLI program that we wrote previously. Let me show you a template for the minimal Flask endpoint we can create

As you can see the structure is really simple. Apart from setting the blueprint, which is the way Flask registers endpoints, we create a simple function that runs the endpoint, and we decorate it assigning the enpoint /rooms that serves GET requests. The function will run some logic and eventually return a Response that contains JSON data, the correct MIME type, and an HTTP status that represents the success or failure of the logic.

The above template becomes the following code

Please note that I initialised the memory storage with the same list used for the script cli.py. Again, the need of initialising the storage with data (even with an empty list) is due to the limitations of the storage MemRepo. The code that runs the use case is

which is exactly the same code that we used in the command-line interface. The last part of the code creates a proper HTTP response, serializing the result of the use case using RoomJsonEncoder, and setting the HTTP status to 200 (success)

This shows you the power of the clean architecture in a nutshell. Writing a CLI interface or a Web service is different only in the presentation layer, not in the logic, which is the same, as it is contained in the use case.

Now that we defined the endpoint, we can finalise the configuration of the webserver, so that we can access the endpoint with a browser. This is not strictly part of the clean architecture, but as I did with the CLI interface I want you to see the final result, to get the whole picture and also to enjoy the effort you put in following the whole discussion up to this point.

## WSGI
Python web applications expose a common interface called Web Server Gateway Interface or WSGI. So to run the Flask development web server, we have to define a wsgi.py file in the main folder of the project, i.e. in the same directory of the file cli.py

When you run the Flask Command Line Interface (documentation), it automatically looks for a file named wsgi.py and loads it, expecting it to contain a variable named app that is an instance of the object Flask. As the function create_app is a factory we just need to execute it.

At this point, you can execute FLASK_CONFIG="development" flask run in the directory that contains this file and you should see a nice message like

At this point, you can point your browser to http://127.0.0.1:5000/rooms and enjoy the JSON data returned by the first endpoint of your web application.

I hope you can now appreciate the power of the layered architecture that we created. We definitely wrote a lot of code to "just" print out a list of models, but the code we wrote is a skeleton that can easily be extended and modified. It is also fully tested, which is a part of the implementation that many software projects struggle with.

The use case I presented is purposely very simple. It doesn't require any input and it cannot return error conditions, so the code we wrote completely ignored input validation and error management. These topics are however extremely important, so we need to discuss how a clean architecture can deal with them.
