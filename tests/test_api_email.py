import factory
from pytest_factoryboy import register

from jublia_email_autosend.models import Email, Recipient
from datetime import datetime, timedelta
import pytz

url_path = "/save_emails"

@register
class EmailFactory(factory.Factory):

    event_id = factory.Sequence(lambda n: '%d' % n)
    email_content = factory.Sequence(lambda n: 'Content of email (%d)' % n)
    email_subject = factory.Sequence(lambda n: 'Content of email (%d)' % n)
    timestamp = datetime.now()
    
    class Meta:
        model = Email

@register
class RecipientFactory(factory.Factory):

    email = factory.Sequence(lambda n: 'user(%d)@gmail.com' % n)
    full_name = factory.Sequence(lambda n: 'Username (%d)' % n)
    
    class Meta:
        model = Recipient

def test_get_email(client, db, recipient_factory, email_factory):
    # test not registered email
    rep = client.get(url_path+"email@notfound.com")
    assert rep.status_code == 404

    # test invalid email
    #rep = client.get(url_path+"invalidemail")
    #assert rep.status_code == 400

def test_get_all_email(client, db, recipient_factory, email_factory):
    recipients = recipient_factory.create_batch(2)

    db.session.add_all(recipients)
    db.session.commit()

    emails = email_factory.create_batch(30)

    db.session.add_all(emails)
    db.session.commit()

    rep = client.get(url_path)
    assert rep.status_code == 200

    results = rep.get_json()
    for email in emails:
        assert any(u['id'] == email.id for u in results['results'])

def test_create_email(client, db, recipient_factory):
    recipients = recipient_factory.create_batch(2)

    db.session.add_all(recipients)
    db.session.commit()
    
    # test bad data
    timestamp = datetime.now(pytz.timezone('Asia/Singapore')) + timedelta(minutes=2)
    timestamp = timestamp.strftime("%d %b %Y %H:%M")
    data = {
        "email_content": "Content of Email",
        "email_subject": "Subject of Email",
        "timestamp": timestamp

    }
    rep = client.post(
        url_path,
        json=data
    )
    assert rep.status_code == 422
    
    # test valid data
    data['event_id'] = 555

    rep = client.post(
        url_path,
        json=data
    )
    assert rep.status_code == 201

    resp_data = rep.get_json()
    email = db.session.query(Email).filter_by(event_id=data['event_id']).first()

    assert email.email_content == resp_data['email']['email_content']
    assert email.event_id == resp_data['email']['event_id']

    # test non-valid timestamp (passed datetime)
    data['timestamp'] = "21 Sep 2010 20:20"
    data['event_id'] = 123
    rep = client.post(
        url_path,
        json=data
    )
    resp_data = rep.get_json()
    assert rep.status_code == 400
    assert resp_data['msg'] == "timestamp must be after email creation time"