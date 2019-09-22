# jublia_email_sending
This Flask based RESTFul API integrates with Celery and RabbitMQ for sending email to a group of recipients, automatically at specific time. Project is a Flask based on a [cookiecuter](https://raw.githubusercontent.com/karec/cookiecutter-flask-restful/). I did some modifications like removing JWT authentication support to match required task assignment as requested by Jublia team.

## Introduction
This cookie cutter is a very simple boilerplate for starting a REST api using Flask, flask-restful, marshmallow, and SQLAlchemy. By default, this project use SQLite as a database backend, to use other RDBMS you can change database configuration found `.flaskenv`. 
It comes with basic project structure and configuration, including blueprints, application factory and basics unit tests.
Celery used for email sending task queues that made via RESTFul API, the task then will be forwarded to RabbitMQ for sending email at later time. Features that you will find in this project.

* Simple flask application using application factory, blueprints
* [Flask command line interface](http://flask.pocoo.org/docs/1.0/cli/) integration
* Simple cli implementation with basics commands (init, run, etc.)
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) included in entry point
* Simple pagination utils
* Unit tests using pytest and factoryboy
* Configuration using environment variables
* OpenAPI json file and swagger UI for easier API Testing and Documentation
* Celery Flower is a web based tool for monitoring and administrating Celery clusters.
* RabbitMQ management plugin provides an HTTP-based API for management and monitoring of RabbitMQ nodes and clusters.

Used packages :

* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/)
* [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
* [passlib](https://passlib.readthedocs.io/en/stable/)
* [tox](https://tox.readthedocs.io/en/latest/)
* [pytest](https://docs.pytest.org/en/latest/)
* [factoryboy](http://factoryboy.readthedocs.io/en/latest/)
* [dotenv](https://github.com/theskumar/python-dotenv)
* [apispec](https://github.com/marshmallow-code/apispec)
* [Flask-Mail](https://github.com/marshmallow-code/apispec)
* [Celery](https://github.com/celery/celery/)
* [Celery Flower](https://github.com/mher/flower/zipball/master#egg=flower)

## System requirements
Make sure that you have all these software installed in your machine to run this project successfully

* Python 3, you can find installation instructions at [this link](https://realpython.com/installing-python/) or via official Python documentation. Tested at Python 3.7.3
* Virtualenv, a tool for Python isolated virtualenv environment creation, installation installation can be found at [this link](https://virtualenv.pypa.io/en/latest/installation/)
* Cookiecutter, a tool for easier project creation whith ready to use template. 
* [Optional] Docker and Docker compose, some tools for developing project in a container based. Dockerfile and docker-compose.yml available at this project can be used for starter point, not really ready to use for production.

### Optional Tools

#### Swagger UI (Recommended)
You can test API with Swagger UI by visiting [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui).

#### RabbitMQ
Run this command to enable RabbitMQ plugin, `sudo` may be needed when executing this command
```
rabbitmq-plugins enable rabbitmq_management
```
Dashabord for managing and monitoring messages queue can be accessed at `http://{node-hostname}:15672/`, by default if you run at localhost, you can access it via[http://localhost:15672/](http://localhost:15672/). Default username and password are: `guest`.
Full instructions on how to enable this plugin can be found at [this link](https://www.rabbitmq.com/management.html)

#### Celery Flower
Celery Flower integration in this ready to use and can be accessed at [http://localhost:5555/](http://localhost:5555/)

**WARNING**: Most of commands are all valid Linux commands due to process development I did on a Linux machine.

## Usage

### Installation
Once you cloned this project, run below commands to setup the project at your local machine
```
cd jublia_email_sending
pip install -r requirements.txt
pip install -e .
```

You have now access to cli commands and you can init your project

```
jublia_email_autosend init # initiate application
```

To list all available commands

```
jublia_email_autosend --help
```


Make sure that `run_celery_worker.sh` is executable. If it is not, run command below:
```
chmod +x run_celery_worker.sh
``` 

### Configuration
You can configure by copying contens of `.flaskenv_template` to a new file `.flaskenv`. Configuration is handled by environment variables, for development purpose you jusst
need to update / add entries in `.flaskenv` file.

It's filled by default with following content:

```
FLASK_ENV=development
FLASK_APP="myapp.app:create_app"
SECRET_KEY=changeme
DATABASE_URI="sqlite:////tmp/myapp.db"
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
```

### Email Configuration

Gmail notice here

FLASK_MAIL Configuration here

Avaible configuration keys:

* `FLASK_ENV`: flask configuration key, enables `DEBUG` if set to `development`
* `SECREY_KEY`: your application secret key
* `DATABASE_URI`: SQLAlchemy connection string
* `CELERY_BROKER_URL`: URL to use for celery broker, only when you enabled celery
* `CELERY_RESULT_BACKEND_URL`: URL to use for celery result backend (e.g: `redis://localhost`)

### Running tests

Simplest way to run tests is to use tox, it will create a virtualenv for tests, install all dependencies and run pytest

```
tox
```

But you can also run pytest manually, you just need to install tests dependencies before

```
pip install pytest pytest-runner pytest-flask pytest-factoryboy factory_boy
pytest
```

**WARNING**: you will need to set env variables

### Running (recommended)

Run this project by executing this command
```
jublia_email_autosend run
```
 By default, project will run at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Running with gunicorn

This project provide a simple wsgi entry point to run gunicorn or uwsgi for example.

For gunicorn you only need to run the following commands

```
pip install gunicorn
gunicorn myapi.wsgi:app
```

And that's it ! Gunicorn is running on port 8000

### Running with uwsgi

Pretty much the same as gunicorn here

```
pip install uwsgi
uwsgi --http 127.0.0.1:5000 --module myapi.wsgi:app
```

And that's it ! Uwsgi is running on port 5000


### Using Flask CLI

This cookiecutter is fully compatible with default flask CLI and use a `.flaskenv` file to set correct env variables to bind the application factory.
Note that we also set `FLASK_ENV` to `development` to enable debugger.


### Using Celery

This cookiecutter has an optional [Celery](http://www.celeryproject.org/) integration that let you choose if you want to use it or not in your project.
If you choose to use Celery, additionnal code and files will be generated to get started with it.

This code will include a dummy task located in `yourproject/yourapp/tasks/example.py` that only return `"OK"` and a `celery_app` file used to your celery workers.

### (Linux user)
RUN WITH SCRIPT

#### Running celery workers

In your project path, once dependencies are installed, you can just run

```
celery worker -A myapi.celery_app:app --loglevel=info
```

If you have updated your configuration for broker / result backend your workers should start and you should see the example task avaible

```
[tasks]
  . myapi.tasks.example.dummy_task
```

#### Running a task

To run a task you can either import it and call it

```python
>>> from myapi.tasks.example import dummy_task
>>> result = dummy_task.delay()
>>> result.get()
'OK'
```

Or use the celery extension

```python
>>> from myapi.extensions import celery
>>> celery.send_task('myapi.tasks.example.dummy_task').get()
'OK'
```

## Using docker (Not recommended)

**WARNING** both Dockerfile and `docker-compose.yml` are **NOT** suited for production, use them for development only or as a starting point.

This template offer simple docker support to help you get started and it comes with both Dockerfile and a `docker-compose.yml`. Please note that docker-compose is mostly useful when using celery
since it takes care of running rabbitmq, redis, your web API and celery workers at the same time, but it also work if you don't use celery at all.

Dockerfile has intentionally no entrypoint to allow you to run any command from it (server, shell, init, celery, ...)

Note that you still need to init your app on first start, even when using compose.

```bash
docker build -t myapp .
...
docker run --env-file=.flaskenv myapp myapi init
docker run --env-file=.flaskenv -p 5000:5000 myapp myapi run -h 0.0.0.0
 * Serving Flask app "myapi.app:create_app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 214-619-010
```

With compose

```bash
docker-compose up
...
docker exec -it <container_id> myapi init
```

## Some things to notice

#### apispec and APISpec-WebFramework is not fully compatible 
Here are some things I found when developing this project
* Most recent version of apispec-webframework is not compatible with most recent version of apispec (3.0.0), so I set apispec version to 0.2.0 to get things work successfully.