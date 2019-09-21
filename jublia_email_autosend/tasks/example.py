from jublia_email_autosend.extensions import celery

@celery.task
def dummy_task():
    return "OK"
