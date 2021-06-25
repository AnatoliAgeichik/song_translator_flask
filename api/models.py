from .config import db

track_singers = db.Table('track_singers', db.metadata,
                      db.Column('Singer_id', db.Integer, db.ForeignKey('singer.id')),
                      db.Column('Track_id', db.Integer, db.ForeignKey('track.id')))


class Singer(db.Model):
    __tablename__ = 'singer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Singer %s>' % self.name


class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    text = db.Column(db.Text)
    original_language = db.Column(db.String(2), default='en')
    singer = db.relationship('Singer', secondary=track_singers, backref=db.backref('Track', lazy='dynamic'))


class Translation(db.Model):
    __tablename__ = 'translation'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    text = db.Column(db.Text)
    language = db.Column(db.String(2), default='en')
    auto_translate = db.Column(db.Boolean, default=True)
