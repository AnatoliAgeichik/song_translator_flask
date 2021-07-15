from .config import ma


class SingerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "created_timestamp", "update_timestamp", "owner_id")


singer_schema = SingerSchema()
singers_schema = SingerSchema(many=True)


class TrackSchema(ma.Schema):
    singers = ma.Nested(SingerSchema(only=("name",)), many=True)

    class Meta:
        fields = (
            "id",
            "name",
            "text",
            "created_timestamp",
            "update_timestamp",
            "singers",
            "owner_id",
        )


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)


class TranslationSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "track_id",
            "text",
            "language",
            "auto_translate",
            "created_timestamp",
            "update_timestamp",
            "owner_id",
        )


translation_schema = TranslationSchema()
translations_schema = TranslationSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "public_id",
            "name",
            "admin",
            "created_timestamp",
            "password",
            "update_timestamp",
        )


user_schema = UserSchema()
