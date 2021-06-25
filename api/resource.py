from flask import request
from flask_restful import Resource
from google_trans_new import google_translator

from .config import db
from .models import Singer, Track, Translation
from .schema import singers_schema, singer_schema, track_schema, tracks_schema, translation_schema, translations_schema


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
    return translator.translate(track.text, lang_tgt=request.json["language"], lang_src=track.original_language)


class SingerListResource(Resource):
    def get(self):
        singers = Singer.query.all()
        return singers_schema.dump(singers)

    def post(self):
        new_singer = Singer(
            name=request.json['name']
        )
        db.session.add(new_singer)
        db.session.commit()
        return singer_schema.dump(new_singer)


class SingerResource(Resource):
    def get(self, id):
        singer = Singer.query.get_or_404(id)
        return singer_schema.dump(singer)

    def put(self, id):
        singer = Singer.query.get_or_404(id)
        singer.name = request.json['name']
        db.session.commit()
        return singer_schema.dump(singer)

    def delete(self, id):
        db.session.delete(Singer.query.get_or_404(id))
        db.session.commit()
        return '', 204


class TrackListResource(Resource):
    def get(self):
        tracks = Track.query.all()
        return tracks_schema.dump(tracks)

    def post(self):
        new_track = Track(
            name=request.json['name'],
            text=request.json['text'],
            original_language=request.json['original_language'],
            singer=get_singers_from_name(request.json['singer'])
        )

        db.session.add(new_track)
        db.session.commit()
        return track_schema.dump(new_track)


class TrackResource(Resource):
    def get(self, id):
        track = Track.query.get_or_404(id)
        return track_schema.dump(track)

    def put(self, id):
        track = Track.query.get_or_404(id)
        track.name = request.json['name']
        track.text = request.json['text']
        track.original_language = request.json['original_language']
        track.singer = get_singers_from_id(request.json['singer'])
        db.session.commit()
        return track_schema.dump(track)

    def delete(self, id):
        db.session.delete(Track.query.get_or_404(id))
        db.session.commit()
        return '', 204


class TranslationListResource(Resource):
    def get(self, id):
        translation = Translation.query.filter_by(track_id=id).all()
        return translations_schema.dump(translation)

    def post(self, id):
        if request.json['auto_translate']:
            text = get_translation(id)
        else:
            text = request.json['text']

        new_translation = Translation(
            text=text,
            language=request.json['language'],
            auto_translate=request.json['auto_translate'],
            track_id=id
        )
        db.session.add(new_translation)
        db.session.commit()
        return translation_schema.dump(new_translation)


class TranslationResource(Resource):
    def get(self, id, transl_id):
        translation = Translation.query.get_or_404(transl_id)
        return translation_schema.dump(translation)

    def put(self, id, transl_id):
        translation = Translation.query.get_or_404(transl_id)

        if request.json['auto_translate']:
            translation.text = get_translation(id)
        else:
            translation.text = request.json['text']

        translation.auto_translate = request.json['auto_translate']
        translation.language = request.json['language']
        translation.track_id = id
        db.session.commit()
        return translation_schema.dump(translation)

    def delete(self, id, transl_id):
        db.session.delete(Translation.query.get_or_404(id))
        db.session.commit()
        return '', 204
