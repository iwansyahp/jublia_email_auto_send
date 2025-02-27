from flask import Flask, redirect

from jublia_email_autosend import api
from jublia_email_autosend.extensions import db, migrate, apispec, celery, mail


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('jublia_email_autosend')
    app.config.from_object('jublia_email_autosend.config')

    if testing is True:
        app.config['TESTING'] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_blueprints(app)
    init_celery(app)
    init_mail(app)

    # add default app url redirection
    app.add_url_rule("/", "root", go_to_swagger_ui)
    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app)
    apispec.spec.components.schema(
        "PaginatedResult", {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }})


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def init_mail(app=None):
    app = app or create_app()
    mail.init_app(app)
    return mail


# auto redirect root-url to /swagger-ui
def go_to_swagger_ui():
    return redirect('/swagger-ui')
