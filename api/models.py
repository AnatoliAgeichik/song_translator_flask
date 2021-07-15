import datetime
from sqlalchemy import func
from sqlalchemy import event
from sqlalchemy.orm import Session

from .config import app, db


def orm_log_after(tablename, method, owner_id, id):
    app.logger.debug(f"user_id {owner_id} finished {method} a {tablename} {id}")


def orm_log_rollback(tablename, method, owner_id, id):
    app.logger.debug(
        f"user_id {owner_id} finished {method} a {tablename} {id} rollback"
    )


track_singers = db.Table(
    "track_singers",
    db.metadata,
    db.Column("singer_id", db.Integer, db.ForeignKey("singer.id")),
    db.Column("track_id", db.Integer, db.ForeignKey("track.id")),
    db.Column(
        "create_timestamp",
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    ),
    db.Column(
        "update_timestamp",
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)


class Base(db.Model):
    __abstract__ = True

    created_timestamp = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    update_timestamp = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Singer(Base):
    __tablename__ = "singer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Singer %s>" % self.name


class Track(Base):
    __tablename__ = "track"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    original_language = db.Column(db.String(2), default="en", nullable=False)
    singers = db.relationship(
        Singer, secondary=track_singers, backref=db.backref("track", lazy="dynamic")
    )
    singer_id = db.Column(db.Integer, db.ForeignKey("singer.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Translation(Base):
    __tablename__ = "translation"

    track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    text = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.CHAR(2), default="en", nullable=False)
    auto_translate = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)


@event.listens_for(Session, "after_flush")
def after_flush(session, flush_context):

    try:
        for obj in session.new:
            orm_log_after(obj.__table__, "create", obj.owner_id, obj.id)
        for obj in session.deleted:
            orm_log_after(obj.__table__, "delete", obj.owner_id, obj.id)
        for obj in session.dirty:
            orm_log_after(obj.__table__, "update", obj.owner_id, obj.id)
    except AttributeError as e:
        app.logger.error(str(e))


@event.listens_for(Session, "after_rollback")
def after_soft_rollback(session):
    for obj in session.new:
        orm_log_rollback(obj.__table__, "create", obj.owner_id, obj.id)
    for obj in session.deleted:
        orm_log_rollback(obj.__table__, "delete", obj.owner_id, obj.id)
    for obj in session.dirty:
        orm_log_rollback(obj.__table__, "update", obj.owner_id, obj.id)
