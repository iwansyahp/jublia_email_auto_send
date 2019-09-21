from jublia_email_autosend.app import app
from jublia_email_autosend.extensions import celery, mail
from flask_mail import Message
from jublia_email_autosend.models import Recipient

@celery.task
def send_email_task(event_id, email_subject, email_content):
    '''Celery Task to send an email to recipients group at certain time, based on timestamp value
    '''
    """Background task to send an email with Flask-Mail."""
    print("Nilai app: ", app.config)
    # TODO: Get email by event_id
    if app is not None:
        # get all recipients
        with app.app_context():
            if mail is not None:
                    recipients = Recipient.query.all()
                    for r in recipients:
                        # create Message object
                        msg = Message("Interview Task at Jublia",
                            sender=("Iwansyah Putra's Task Assignment", "coffeefarm.id@gmail.com"),
                            recipients=[r.email])
                        msg.body = '''Hi, %s. This email was sent by a Flask app integrated RabbitMQ and Celery''' % r.full_name                
                        # send email one-by-one
                        mail.send(msg)
            else:
                print("Nilai mail ",mail)
                print('Please setup email client correctly')
    else:
        print("App instance is not found")