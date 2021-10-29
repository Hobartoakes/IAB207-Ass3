from werkzeug.security import generate_password_hash
import datetime
from . import db
from . import models

def init(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add(models.User(
            email="test@test.com",
            password=generate_password_hash("123123", method='sha256'),
            name="test",
            contact="13333333333",
            address="NewYork"
        ))

        db.session.add(models.Event(
            id=1,
            type="Country",
            title="Introducing ARSM",
            desc="Wherever you are in the world, join us for a free webinar about our performance-only diploma.",
            image_path="event1.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=2,
            type="Pop",
            title="Take Back The Nights",
            desc="Take Back The Nights Light The Future 2021.",
            image_path="event2.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=3,
            type="R&B",
            title="ONLINE DANCE PARTY",
            desc="*** ONLINE DANCE PARTY *** FREE on ZOOM!",
            image_path="event3.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=4,
            type="R&B",
            title="Online Reggae Radio",
            desc="Online Reggae Radio | Culture Vibes Show | Broadcast | Listeners Shoutout!",
            image_path="event4.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=5,
            type="Jazz",
            title="Session 157 - Wild Horses",
            desc="Session 157 - Wild Horses - The Rolling Stones",
            image_path="event5.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=6,
            type="Pop",
            title="Toddler Songs and Rhymes",
            desc="Toddler Songs and Rhymes | Early READ",
            image_path="event6.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=7,
            type="Jazz",
            title="80s Music Trivia",
            desc="80s Music Trivia - Presented by Thinker Themed Trivia, Sponsored by Mountie",
            image_path="event7.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=8,
            type="Country",
            title="Laura Hall & Rick Hall",
            desc="Laura Hall & Rick Hall - SBCCA Live Stream",
            image_path="event8.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.add(models.Event(
            id=9,
            type="Pop",
            title="Pop Music History",
            desc="Pop Music History Comes Alive",
            image_path="event9.jpg",
            date=datetime.datetime.now(),
            status="Upcoming",
            created="test@test.com"
        ))

        db.session.commit()
