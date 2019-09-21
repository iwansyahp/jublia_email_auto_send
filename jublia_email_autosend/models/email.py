from jublia_email_autosend.extensions import db
from datetime import datetime, timedelta

class Email(db.Model):
    """Basic email model
    """
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False, unique=True)
    email_subject = db.Column(db.String(200), nullable=False)
    email_content = db.Column(db.String(2000), nullable=False)
    timestamp = db.Column(db.TIMESTAMP(), nullable=False)

    def __init__(self, **kwargs):
        super(Email, self).__init__(**kwargs)

    def __repr__(self):
        return "<Email %s>" % self.event_id
