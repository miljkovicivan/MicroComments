'''
Resources used in comments service
'''
from flask_mongorest.resources import Resource
from documents import User, Comment
from flask_mongorest import operators as ops


class UserResource(Resource):
    """
    User resource class
    """
    document = User


class CommentResource(Resource):
    """
    Comment resource class
    """
    document = Comment
    filters = {
        'entity_id': [ops.Exact],
        'entity_class': [ops.Exact],
    }
    related_resources = {
        'user': UserResource
    }