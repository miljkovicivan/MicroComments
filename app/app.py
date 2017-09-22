'''
App configs and view
'''
import datetime
import os
import flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_cors import CORS
from flask_mongorest import methods, views
from resources import CommentResource
from authentification import JwtTokenAuthentication
from db import DB


APP = flask.Flask(__name__)

ENV = os.getenv('ENV', 'local')

if ENV == 'ci':
    APP.config.from_pyfile('configs/circleci.conf')
elif ENV == 'production':
    APP.config.from_pyfile('configs/production.conf')
else:
    APP.config.from_pyfile('configs/local.conf')

APP.secret_key = APP.config.get('SECRET_KEY')

API = MongoRest(APP)

DB.init_app(APP)

CORS = CORS(APP, resources={r"/comments/*": {"origins": "*"}})


@API.register(name='comments', url='/comments/')
class CommentView(views.ResourceView):
    """
    Comment view class
    """
    authentication_methods = [JwtTokenAuthentication]
    resource = CommentResource
    methods = [
        methods.Create,
        methods.List,
        methods.Fetch,
        methods.Delete,
        methods.Update
    ]

    def put(self, **kwargs):
        from documents import Comment
        ret = super(CommentView, self).put(**kwargs)
        comment = Comment.objects.get(pk=ret['id'])
        comment.last_modified = datetime.datetime.now()
        comment.save()
        ret['last_modified'] = comment.last_modified
        return ret

