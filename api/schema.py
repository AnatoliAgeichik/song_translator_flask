from .config import ma


class SingerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "created_date", "update_date")


singer_schema = SingerSchema()
singers_schema = SingerSchema(many=True)


class TrackSchema(ma.Schema):
    singer = ma.Nested(SingerSchema(only=("name", )), many=True)

    class Meta:
        fields = ("id", "name", "text", "created_date", "update_date", "singer")


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)


class TranslationSchema(ma.Schema):

    class Meta:
        fields = ("id", "track_id", "text", "language", "auto_translate", "created_date", "update_date")


translation_schema = TranslationSchema()
translations_schema = TranslationSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "public_id", "name", "admin", "created_date", "update_date")


user_schema = UserSchema()
