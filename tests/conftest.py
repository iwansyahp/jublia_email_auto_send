import json
import pytest

from jublia_email_autosend.models import Email, Recipient
from jublia_email_autosend.app import create_app
from jublia_email_autosend.extensions import db as _db


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def initial_recipient(db):

    recipient = Recipient(
        email="iwansyahp@gmail.com",
        full_name="Iwansyah Putra"
    )

    db.session.add(recipient)
    db.session.commit()
    
    return recipient
