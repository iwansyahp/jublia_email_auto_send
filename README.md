# JUBLIA AUTOMATIC EMAIL SENDING
This Flask based RESTFul API implements with Celery and RabbitMQ for sending email to a group of email recipients, automatically at specific time.

## Introduction
This cookie cutter is a very simple boilerplate for starting a REST api using Flask, flask-restful, marshmallow, and SQLAlchemy. By default, this project use SQLite as a database backend, to use other RDBMS you can change database configuration in `.flaskenv`. 
It comes with basic Flask project structure and configuration, including blueprints, application factory and unit tests.
Celery used for automatic and scheduled email sending task queues that made by users via RESTFul API, the task then will be forwarded to RabbitMQ for sending email at given time. Features of this project.

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
* RabbitMQ, installation instructions can be found at [this link](https://www.rabbitmq.com/download.html) and choose the system environment. Default RabbitMQ credentials are used in this project (username and password: `guest` at `localhost`)

### Optional Tools

#### Swagger UI (Recommended)
You can test API with Swagger UI to simplify your API testing.

#### RabbitMQ Plugins
Run this command to enable RabbitMQ plugin, `sudo` may be needed when executing this command
```
rabbitmq-plugins enable rabbitmq_management
```
Dashabord for managing and monitoring messages queue can be accessed at `http://{node-hostname}:15672/`, by default if you run at localhost, you can access it via[http://localhost:15672/](http://localhost:15672/). Default username and password are: `guest`.
Full instructions on how to enable this plugin can be found at [this link](https://www.rabbitmq.com/management.html)

#### Celery Flower
Celery Flower integration in this ready to use. Once you run `run_celery_worker_and_flower.sh` successfully, you can access it at [http://localhost:5555/](http://localhost:5555/)

**WARNING**: Most of commands used here are valid Linux commands.

# Usage

## Installation
Once you cloned this project, run below commands to setup the project at your local machine
```
cd jublia_email_sending
```
Create isolated Python virtual environment
```
virtualenv env -p /usr/bin/python3.7, # or whichever python version you have
```
Activate created virtual environment 
```
source env/bin/activate
```
Install all requirements

```
pip install -r requirements.txt
pip install -e . # don't the . (dot) at the end of this command execution
```


### Setting up Configuration and Environment
Create app configure for by copying contens of `.flaskenv_template` to a new file `.flaskenv`.
```
cp .flaskenv_template .flaskenv
```

Configuration is handled by environment variables, for development purpose you jusst
need to update / add entries in `.flaskenv` file.

If you have installed RabbitMQ with non default configuration
Please make sure username and password of installed RabbitMQ configured correctly at .flaskenv and tox.ini

Change necessary value depending on your environment, make sure that value of this variable configured correctly

```
SECRET_KEY
DATABASE_URI
CELERY_BROKER_URL
CELERY_BROKER_BACKENDURL
MAIL_USERNAME
MAIL_PASSWORD
```


You have now access to cli commands and you can init your project

```
jublia_email_autosend init # to initiate application
```

To list all available commands

```
jublia_email_autosend --help
```
Make sure that RabbitMQ service is running by executing this command

```
sudo service rabbitmq-server status
```
If it is not runnig, run execute this command:
```
sudo service rabbitmq-server start
```

Make sure that `run_celery_worker.sh` is executable. If it is not, run command below:
```
chmod +x run_celery_worker.sh
```
## Run Celery Worker
Activate Celery worker and Flower by invoking this command
```
./run_celery_worker_and_flower.sh <email> <password-of-email>
```
Dont forget to change the email and password, leave this terminal open and see all given Celery tasks via the API.

If you prefer to run Celery worker only, make sure that you set MAIL_USERNAME and MAIL_PASSWORD and run this command

Set necessary environment variables
```
exportMAIL_USERNAME=<sender-email-to-be-used>
export MAIL_PASSWORD=<password-of-sender-email>
export DATABASE_URI=sqlite:///jublia_email_autosend.db
```
Run the Celery Worker
```
jublia_email_autosend.celery_app:app --loglevel=info

```

You can visit http://localhost:5555 to see and manage celery clusters and tasks visually via Celery Flower.

### Run Application
Open new terminal and move to project directory. Activate created virtual environment by running 
```
source ./env/bin/activate
```
Run your app by executing this command
```
jublia_email_autosend run
```

If everythings configured correctly and celery worker runs successfully, you can visit:
* http://127.0.0.1:5000/ to see running application (you will redirected to http://127.0.0.1:5000/swagger-ui)
* http://127.0.0.1:5000/swagger-ui to use Swagger UI features and test your API in simple way

Swagger UI list all availables endpoint created in this project, if you prefer to use cURL, these are sample commands:
* Adding new recipient
```
curl -X POST "http://127.0.0.1:5000/recipients" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"email\":\"email_of_recipient\",\"full_name\":\"fullname_of_email_owner\"}" 
```
Dont forget to `change email_of_recipient` and `fullname_of_email_owner`

* Create new email
```
curl -X POST "http://127.0.0.1:5000/save_emails" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"email_content\":\"content_of_email\",\"email_subject\":\"subject_of_email\",\"event_id\":1,\"timestamp\":\"22 Sep 2019 20:50\"}"
```
Dont forget to change necessary value like `content_of_email`, `subject_of_email` and `timestamp`. Timestamp format should be following this format: 
```
22 Sep 2019 20:50
```

Assumed timezone is Asia/Singapore, timestamp must after email message creation time. Email will be sent at given timestamp.

For other cURL commands available at Swagger UI documented API.

### Running unit tests

Simplest way to run tests is to use tox, it will create a virtualenv for tests, install all dependencies and run pytest
```
tox
```

## Some things to notice

#### GMail SMTP Implementation
If you use GMAIL as an SMTP server please make sure that used sender email is configured to:
* Disable Passing Captcha Checking
* Disable 2 Factor Authentications
* Enable Less Secure Apps Access

#### apispec and APISpec-WebFramework is not fully compatible 
Here are some things I found when developing this project
* Most recent version of apispec-webframework is not compatible with most recent version of apispec (3.0.0), so I set apispec version to 0.2.0 to get things work successfully.

#### Initial email recipients
I made initial recipients of the created email, which are my personal emails.