'''
Documents used in comments service
'''
from datetime import datetime
from db import DB


class User(DB.EmbeddedDocument):
    """
    User embedded document class
    """
    user_id = DB.IntField()
    email = DB.StringField(max_length=100)
    first_name = DB.StringField(max_length=100)
    last_name = DB.StringField(max_length=100)


class Comment(DB.Document):
    """
    Comment document class
    """
    entity_id = DB.IntField(required=True)
    entity_class = DB.StringField(max_length=50, required=True)
    content = DB.StringField(required=True)
    creation_date = DB.DateTimeField(default=datetime.now)
    last_modified = DB.DateTimeField(default=datetime.now)
    user = DB.EmbeddedDocumentField(User, required=True)