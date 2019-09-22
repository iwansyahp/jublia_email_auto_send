import factory
from pytest_factoryboy import register

from jublia_email_autosend.models import Email, Recipient
from datetime import datetime, timedelta
import pytz

url_path = "/recipients"


@register
class RecipientFactory(factory.Factory):

    email = factory.Sequence(lambda n: 'user(%d)@gmail.com' % n)
    full_name = factory.Sequence(lambda n: 'Username (%d)' % n)
    
    class Meta:
        model = Recipient

def test_get_recipient(client, db, recipient_factory):
    # test not registered email
    
    rep = client.get(url_path+"email@notfound.com")
    assert rep.status_code == 404

    # test valid emails
    recipients = recipient_factory.create_batch(2)

    db.session.add_all(recipients)
    db.session.commit()

    for r in recipients:
        rep = client.get(url_path+"/"+r.email)
        resp_data = rep.get_json()
        assert rep.status_code == 200
        assert any(resp_data['recipient']['id'] == r.id for r in recipients)


def test_get_all_recipients(client, db, recipient_factory):
    recipients = recipient_factory.create_batch(2)

    db.session.add_all(recipients)
    db.session.commit()

    rep = client.get(url_path)
    assert rep.status_code == 200

    resp_data = rep.get_json()
    for r in recipients:
        assert any(result['id'] == r.id for result in resp_data['results'])
