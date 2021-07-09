from flask import request, jsonify, make_response
from flask_restful import Resource
from google_trans_new import google_translator
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from sqlalchemy import or_

from .config import db, app, pagination
from .models import Singer, Track, Translation, User
from .schema import (
    singers_schema,
    singer_schema,
    track_schema,
    tracks_schema,
    translation_schema,
    translations_schema,
    user_schema,
)
from .services import (
    token_required,
    get_search_value,
    get_sort_parameter_singer,
    get_sort_parameter_track,
    get_sort_parameter_translation,
)


def get_singers_from_name(singers_name):
    singers = []
    for singer_name in singers_name:
        singers.append(Singer.query.filter_by(name=singer_name).first())
    return singers


def get_singers_from_id(singers_id):
    singers = []
    for singer_id in singers_id:
        singers.append(Singer.query.get(singer_id))
    return singers


def get_translation(track_id):
    translator = google_translator()
    track = Track.query.get(track_id)
    return translator.translate(
        track.text, lang_tgt=request.json["language"], lang_src=track.original_language
    )


class SingerListResource(Resource):
    def get(self):
        return pagination.paginate(
            Singer.query.filter(
                Singer.name.ilike(f"%{get_search_value(request)}%")
            ).order_by(get_sort_parameter_singer(request)),
            singers_schema,
            marshmallow=True,
        )

    @token_required
    def post(self, user_id):
        new_singer = Singer(name=request.json["name"], owner_id=user_id)
        db.session.add(new_singer)
        db.session.commit()
        return singer_schema.dump(new_singer)


class SingerResource(Resource):
    def get(self, id):
        return singer_schema.dump(Singer.query.get_or_404(id))

    @token_required
    def put(self, user_id, id):
        singer = Singer.query.get_or_404(id)
        singer.name = request.json["name"]
        db.session.commit()
        return singer_schema.dump(singer)

    @token_required
    def delete(self, user_id, id):
        db.session.delete(Singer.query.get_or_404(id))
        db.session.commit()
        return "", 204


class TrackListResource(Resource):
    def get(self):
        search = get_search_value(request)
        return pagination.paginate(
            Track.query.filter(
                or_(
                    Track.name.ilike(f"%{search}%"),
                    Track.text.ilike(f"%{search}%"),
                    Track.original_language.ilike(f"%{search}%"),
                )
            ).order_by(get_sort_parameter_track(request)),
            tracks_schema,
            marshmallow=True,
        )

    @token_required
    def post(self, user_id):
        new_track = Track(
            name=request.json["name"],
            text=request.json["text"],
            original_language=request.json["original_language"],
            singer=get_singers_from_name(request.json["singer"]),
            owner_id=user_id,
        )

        db.session.add(new_track)
        db.session.commit()
        return track_schema.dump(new_track)


class TrackResource(Resource):
    def get(self, id):
        return track_schema.dump(Track.query.get_or_404(id))

    @token_required
    def put(self, user_id, id):
        track = Track.query.get_or_404(id)
        track.name = request.json["name"]
        track.text = request.json["text"]
        track.original_language = request.json["original_language"]
        track.singer = get_singers_from_id(request.json["singer"])
        db.session.commit()
        return track_schema.dump(track)

    @token_required
    def delete(self, user_id, id):
        db.session.delete(Track.query.get_or_404(id))
        db.session.commit()
        return "", 204


class TranslationListResource(Resource):
    def get(self, id):
        search = get_search_value(request)
        return pagination.paginate(
            Translation.query.filter_by(track_id=id)
            .filter(
                or_(
                    Translation.text.ilike(f"%{search}%"),
                    Translation.language.ilike(f"%{search}%"),
                )
            )
            .order_by(get_sort_parameter_translation(request)),
            translations_schema,
            marshmallow=True,
        )

    @token_required
    def post(self, user_id, id):
        if request.json["auto_translate"]:
            text = get_translation(id)
        else:
            text = request.json["text"]
        new_translation = Translation(
            text=text,
            language=request.json["language"],
            auto_translate=request.json["auto_translate"],
            track_id=id,
            owner_id=user_id,
        )
        db.session.add(new_translation)
        db.session.commit()
        return translation_schema.dump(new_translation)


class TranslationResource(Resource):
    def get(self, id, transl_id):
        return translation_schema.dump(Translation.query.get_or_404(transl_id))

    @token_required
    def put(self, user_id, id, transl_id):
        translation = Translation.query.get_or_404(transl_id)

        if request.json["auto_translate"]:
            translation.text = get_translation(id)
        else:
            translation.text = request.json["text"]

        translation.auto_translate = request.json["auto_translate"]
        translation.language = request.json["language"]
        translation.track_id = id
        db.session.commit()
        return translation_schema.dump(translation)

    @token_required
    def delete(self, user_id, id, transl_id):
        db.session.delete(Translation.query.get_or_404(transl_id))
        db.session.commit()
        return "", 204


class SignupUser(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            password=hashed_password,
            admin=False,
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class LoginUser(Resource):
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response(
                "could not verify",
                401,
                {"WWW.Authentication": 'Basic realm: "login required"'},
            )

        user = User.query.filter_by(name=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
            )
            return jsonify({"token": token})

        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )
