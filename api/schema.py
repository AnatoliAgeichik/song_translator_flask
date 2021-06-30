from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from .models import Singer, Track, Translation, User


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
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    text = auto_field()
    original_language = auto_field()
    singer = auto_field()


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)


class TranslationSchema(SQLAlchemySchema):
    class Meta:
        model = Translation
        load_instance = True

    id = auto_field()
    track_id = auto_field()
    text = auto_field()
    language = auto_field()
    auto_translate = auto_field()


translation_schema = TranslationSchema()
translations_schema = TranslationSchema(many=True)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    public_id = auto_field()
    name = auto_field()
    password = auto_field()
    admin = auto_field()


user_schema = UserSchema()
