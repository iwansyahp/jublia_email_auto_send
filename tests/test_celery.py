import pytest

from jublia_email_autosend.app import init_celery
from jublia_email_autosend.tasks.send_email import send_email_task


@pytest.fixture
def celery_app(celery_app, app):
    celery = init_celery(app)

    celery_app.conf = celery.conf
    celery_app.Task = celery_app.Task

    yield celery_app


def test_example(celery_app, celery_worker):
    """Simply test our dummy task using celery"""
    res = send_email_task.apply_async()
    assert res.get() == "OK"
