from flask import request, jsonify
import jwt
from functools import wraps

from .models import User, Singer, Track, Translation
from .config import app
import os
from dotenv import load_dotenv

load_dotenv()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=os.getenv('JWT_ALGORITHM'))
            if not User.query.filter_by(public_id=data['public_id']).first():
                return jsonify({'message': 'token is invalid'})
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'token is invalid'})
        except jwt.exceptions.InvalidKeyError:
            return jsonify({'message': 'key is invalid'})
        except jwt.exceptions.InvalidAlgorithmError:
            return jsonify({'message': 'algortithm is invalid'})

        return f(*args, **kwargs)

    return decorator


def get_search_value(request):
    return request.args.get('search') if request.args.get('search') else ''


def get_sort_parameter(request):
    return request.args.get('sort')


def get_sort_parameter_singer(request):
    sort = get_sort_parameter(request)
    if sort == 'name':
        return Singer.name.asc()
    elif sort == '-name':
        return Singer.name.desc()


def get_sort_parameter_track(request):
    sort = get_sort_parameter(request)

    if sort == 'name':
        return Track.name.asc()
    elif sort == '-name':
        return Track.name.desc()
    elif sort == 'text':
        return Track.text.asc()
    elif sort == '-text':
        return Track.text.desc()
    elif sort == 'original_language':
        return Track.original_language.asc()
    elif sort == '-original_language':
        return Track.original_language.desc()


def get_sort_parameter_translation(request):
    sort = get_sort_parameter(request)

    if sort == 'text':
        return Translation.text.asc()
    elif sort == '-text':
        return Translation.text.desc()
    elif sort == 'language':
        return Translation.language.asc()
    elif sort == '-language':
        return Translation.language.desc()
