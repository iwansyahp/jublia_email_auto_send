from jublia_email_autosend.extensions import db

class Recipient(db.Model):
    """Basic email recipient model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(2000), unique=True, nullable=False)
    
    def __init__(self, **kwargs):
        super(Recipient, self).__init__(**kwargs)

    def __repr__(self):
        return "<Recipient %s>" % self.email
