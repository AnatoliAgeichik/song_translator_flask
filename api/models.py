import datetime
from sqlalchemy import func
from sqlalchemy import event
from .config import app

from .config import db


def orm_log_after(tablename, method, owner_id, id):
    app.logger.debug(f"user_id {owner_id} finished {method} a {tablename} {id}")


def orm_log_before(tablename, method, owner_id):
    app.logger.debug(f"user_id {owner_id} started {method} a {tablename}")


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
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Singer %s>" % self.name


@event.listens_for(Singer, "after_insert")
def insert_log(mapper, connection, target):
    orm_log_after(
        tablename="singer", method="created", owner_id=target.owner_id, id=target.id
    )


@event.listens_for(Singer, "before_insert")
def insert_log(mapper, connection, target):
    orm_log_before(tablename="singer", method="created", owner_id=target.owner_id)


@event.listens_for(Singer, "before_update")
def update_log(mapper, connection, target):
    orm_log_before(tablename="singer", method="update", owner_id=target.owner_id)


@event.listens_for(Singer, "after_update")
def update_log(mapper, connection, target):
    orm_log_after(
        tablename="singer", method="update", owner_id=target.owner_id, id=target.id
    )


@event.listens_for(Singer, "before_delete")
def delete_log(mapper, connection, target):
    orm_log_before(tablename="singer", method="delete", owner_id=target.owner_id)


@event.listens_for(Singer, "after_delete")
def delete_log(mapper, connection, target):
    orm_log_after(
        tablename="singer", method="delete", owner_id=target.owner_id, id=target.id
    )


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
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@event.listens_for(Track, "after_insert")
def insert_log(mapper, connection, target):
    orm_log_after(
        tablename="track", method="created", owner_id=target.owner_id, id=target.id
    )


@event.listens_for(Track, "before_insert")
def insert_log(mapper, connection, target):
    orm_log_before(tablename="track", method="created", owner_id=target.owner_id)


@event.listens_for(Track, "before_update")
def update_log(mapper, connection, target):
    orm_log_before(tablename="track", method="update", owner_id=target.owner_id)


@event.listens_for(Track, "after_update")
def update_log(mapper, connection, target):
    orm_log_after(
        tablename="track", method="update", owner_id=target.owner_id, id=target.id
    )


@event.listens_for(Track, "before_delete")
def delete_log(mapper, connection, target):
    orm_log_before(tablename="track", method="delete", owner_id=target.owner_id)


@event.listens_for(Track, "after_delete")
def delete_log(mapper, connection, target):
    orm_log_after(
        tablename="track", method="delete", owner_id=target.owner_id, id=target.id
    )


class Translation(Base):
    __tablename__ = "translation"

    track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    text = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.CHAR(2), default="en", nullable=False)
    auto_translate = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@event.listens_for(Translation, "after_insert")
def insert_log(mapper, connection, target):
    orm_log_after(
        tablename="translation",
        method="created",
        owner_id=target.owner_id,
        id=target.id,
    )


@event.listens_for(Translation, "before_insert")
def insert_log(mapper, connection, target):
    orm_log_before(tablename="translation", method="created", owner_id=target.owner_id)


@event.listens_for(Translation, "before_update")
def update_log(mapper, connection, target):
    orm_log_before(tablename="translation", method="update", owner_id=target.owner_id)


@event.listens_for(Translation, "after_update")
def update_log(mapper, connection, target):
    orm_log_after(
        tablename="translation", method="update", owner_id=target.owner_id, id=target.id
    )


@event.listens_for(Translation, "before_delete")
def delete_log(mapper, connection, target):
    orm_log_before(tablename="translation", method="delete", owner_id=target.owner_id)


@event.listens_for(Translation, "after_delete")
def delete_log(mapper, connection, target):
    orm_log_after(
        tablename="translation", method="delete", owner_id=target.owner_id, id=target.id
    )


class User(Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)
