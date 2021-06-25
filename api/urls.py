from flask_restful import Api
from .resource import SingerListResource, SingerResource, TrackListResource, TrackResource, TranslationListResource, \
                      TranslationResource
from .config import app


api = Api(app)

api.add_resource(SingerListResource, '/singers')
api.add_resource(SingerResource, '/singers/<int:id>')
api.add_resource(TrackListResource, '/tracks')
api.add_resource(TrackResource, '/tracks/<int:id>')
api.add_resource(TranslationListResource, '/tracks/<int:id>/translations')
api.add_resource(TranslationResource, '/tracks/<int:id>/translations/<int:transl_id>')
