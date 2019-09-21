"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from flask_mail import Mail

from jublia_email_autosend.commons.apispec import APISpecExt


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
celery = Celery()
mail = Mail()
