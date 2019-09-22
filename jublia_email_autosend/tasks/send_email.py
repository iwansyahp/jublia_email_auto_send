from flask import current_app as app
from jublia_email_autosend.extensions import celery, mail
from flask_mail import Message
from jublia_email_autosend.models import Recipient, Email


@celery.task
def send_email_task(id):
    '''Celery Task to send an email to recipients group at certain time, based on timestamp value
    '''
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        email = Email.query.get(id)
        print("email_id pada task", email.id)
        if email:
            if app is not None:
                # get all recipients
                if mail is not None:
                    recipients = Recipient.query.all()

                    for r in recipients:
                        print(r.email)
                    # create Message object
                    msg = Message(
                        email.email_subject,
                        sender=("Iwansyah Putra", "coffeefarm.id@gmail.com"),
                        recipients=[r.email for r in recipients])
                    msg.body = email.email_content
                    mail.send(msg)
                    return "Email with id %d sent." % id
                else:
                    print("Nilai mail ", mail)
                    print('Please setup email client correctly')
        else:
            print("Email with id=%d deleted" % id)
