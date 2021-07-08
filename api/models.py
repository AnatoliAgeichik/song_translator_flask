import datetime
from sqlalchemy import func
from .config import db

track_singers = db.Table(
    "track_singers",
    db.metadata,
    db.Column("Singer_id", db.Integer, db.ForeignKey("singer.id")),
    db.Column("Track_id", db.Integer, db.ForeignKey("track.id")),
)


class Base(db.Model):
    __abstract__ = True

    created_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    update_date = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Singer(Base):
    __tablename__ = "singer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Singer %s>" % self.name


class Track(Base):
    __tablename__ = "track"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    original_language = db.Column(db.String(2), default="en", nullable=False)
    singer = db.relationship(
        "Singer", secondary=track_singers, backref=db.backref("track", lazy="dynamic")
    )
    singer_id = db.Column(db.Integer, db.ForeignKey("singer.id"))


class Translation(Base):
    __tablename__ = "translation"

    track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    text = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.CHAR(2), default="en", nullable=False)
    auto_translate = db.Column(db.Boolean, default=True)


class User(Base):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)
