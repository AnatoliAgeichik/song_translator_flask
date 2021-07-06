import datetime
from sqlalchemy import func
from .config import db

track_singers = db.Table('track_singers', db.metadata,
                      db.Column('Singer_id', db.Integer, db.ForeignKey('singer.id')),
                      db.Column('Track_id', db.Integer, db.ForeignKey('track.id')))


class Base:
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Singer(db.Model, Base):
    __tablename__ = 'singer'

    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Singer %s>' % self.name


class Track(db.Model, Base):
    __tablename__ = 'track'

    name = db.Column(db.String(64))
    text = db.Column(db.Text)
    original_language = db.Column(db.String(2), default='en')
    singer = db.relationship('Singer', secondary=track_singers, backref=db.backref('track', lazy='dynamic'))


class Translation(db.Model, Base):
    __tablename__ = 'translation'

    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    text = db.Column(db.Text)
    language = db.Column(db.CHAR(2), default='en')
    auto_translate = db.Column(db.Boolean, default=True)


class User(db.Model, Base):
    public_id = db.Column(db.String(200))
    name = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    admin = db.Column(db.Boolean, default=False)
