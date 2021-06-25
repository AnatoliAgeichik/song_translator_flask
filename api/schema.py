from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from .models import Singer, Track


class SingerSchema(SQLAlchemySchema):
    class Meta:
        model = Singer
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()


singer_schema = SingerSchema()
singers_schema = SingerSchema(many=True)


class TrackSchema(SQLAlchemySchema):
    class Meta:
        model = Track

        load_instance = True

    id = auto_field()
    name = auto_field()
    text = auto_field()
    original_language = auto_field()
    singer = auto_field()


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)