from url_shortener.core import db
import random


class Shortener(db.Model):

    __tablename__ = 'shortener'

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(1000), nullable=False, unique=True)
    short_url = db.Column(db.String(200), nullable=False, unique=True)
    hits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    @staticmethod
    def create_short_url(long_url):
        short_url = Shortener.unique_value_generation()
        shortener = Shortener(
            long_url=long_url,
            short_url=short_url
        )
        db.session.add(shortener)
        db.session.commit()
        return short_url

    @staticmethod
    def unique_value_generation():
        length = 7
        short_value = ''
        s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Basically trimming to the length
        for i in range(length):
            rand = random.Random()
            short_value += rand.choice(s)

        # Checking this random value is not available in the system
        if Shortener.query.filter_by(short_url=str(short_value)).first() is not None:
            short_url = Shortener.unique_value_generation()

        return str(short_value)

    def to_json(self):
        return {
            'id': self.id,
            'long_url': self.long_url,
            'short_url': self.short_url,
            'hits': self.hits,
            'date_Created': self.date_created
        }
