"""
CRUD and filter tests
"""
import json
import unittest
from unittest.mock import MagicMock
from flask_mongoengine import MongoEngine
from app import APP
from authentification import JwtTokenAuthentication
from documents import Comment, User


DB = MongoEngine()
APP.config.from_pyfile('configs/testing.conf')
DB.init_app(APP)


class UnauthorizedTestCase(unittest.TestCase):
    """
    Regular authorization
    """
    pass


class AuthorizedTestCase(unittest.TestCase):
    """
    Mocked authorization
    """

    def setUp(self):
        self.authorized = JwtTokenAuthentication.authorized
        JwtTokenAuthentication.authorized = MagicMock(return_value=True)

    def tearDown(self):
        JwtTokenAuthentication.authorized = self.authorized


class CRUDUnauthorizedTestCase(UnauthorizedTestCase):
    """
    Checks that all methods are rejected
    """

    def setUp(self):
        super(CRUDUnauthorizedTestCase, self).setUp()
        self.APP = APP.test_client()
        self.dummy_pk = '111111111111111111111111'

    def test__get(self):
        """
        Test get is rejected
        """
        response = self.APP.get('/comments/')
        self.assertEqual(response.status_code, 401)

    def test__post(self):
        """
        Test post is rejected
        """
        response = self.APP.post('/comments/')
        self.assertEqual(response.status_code, 401)

    def test__delete(self):
        """
        Test delete is rejected
        """
        response = self.APP.delete('/comments/%s/' % self.dummy_pk)
        self.assertEqual(response.status_code, 401)

    def test__put(self):
        """
        Test put is rejected
        """
        response = self.APP.put('/comments/%s/' % self.dummy_pk)
        self.assertEqual(response.status_code, 401)


class CRUDTestCase(AuthorizedTestCase):
    """
    Test functionality
    """

    def setUp(self):
        super(CRUDTestCase, self).setUp()
        self.APP = APP.test_client()
        self.header = {'Content-Type:': 'APPlication/json'}

        self.entity_id = 1
        self.entity_class = 'Booking'
        self.user = User()
        self.content = 'test content'

        self.user = User(
            email='asd',
            last_name='asd',
            first_name='asd',
            user_id=1
        )

    def test__post_without_parametes(self):
        """
        Test post with missing parameters
        """

        post_data = {'entity_id': 1}
        missing_fields = ['content', 'entity_class']

        response = self.APP.post(
            '/comments/',
            data=json.dumps(post_data),
            headers={
                'Content-Type': 'APPlication/json'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)['field-errors']
        for field_name in missing_fields:
            self.assertEqual(data[field_name], 'Field is required')
        self.assertEqual(len(missing_fields)+1, len(data.keys()))

    def test__post(self):
        """
        Test regular post
        """

        fields = [
            'user',
            'entity_class',
            'entity_id',
            'creation_date',
            'last_modified',
            'id',
            'content'
            ]
        post_data = {
            'entity_id': self.entity_id,
            'entity_class': self.entity_class,
            'user': {
                'first_name': 'pera',
                'last_name': 'zika',
                'user_id': 123,
                'email': 'asd',
                },
            'content': self.content,
            }

        response = self.APP.post(
            '/comments/',
            data=json.dumps(post_data),
            headers={'Content-Type': 'APPlication/json'}
            )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for field in fields:
            self.assertTrue(field in data.keys())
        self.assertEqual(len(fields), len(data.keys()))

    def test__get_one(self):
        """
        Test get one comment
        """

        Comment.objects.all().delete()
        comment = Comment(
            user=self.user,
            entity_id=self.entity_id,
            entity_class=self.entity_class,
            content=self.content
            )
        comment.save()
        comment_pk = Comment.objects.first().pk

        response = self.APP.get(
            '/comments/%s/' % comment_pk,
            headers={'Content-Type': 'APPlication/json'}
            )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        comment = Comment.objects.get(pk=data['id'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.entity_class, self.entity_class)
        self.assertEqual(comment.entity_id, self.entity_id)
        self.assertEqual(comment.content, self.content)

    def test__put(self):
        """
        Test regular put
        """

        put_data = {'content': 'new content'}

        # with switch_DB(Comment, 'testing') as Comment:
        comment_pk = Comment.objects.first().pk

        response = self.APP.put(
            '/comments/%s/' % comment_pk,
            data=json.dumps(put_data),
            headers={'Content-Type': 'APPlication/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        comment = Comment.objects.get(pk=data['id'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.entity_class, self.entity_class)
        self.assertEqual(comment.entity_id, self.entity_id)
        self.assertEqual(comment.content, put_data['content'])

    def test__delete(self):
        """
        Test regular delete
        """

        # make sure that at least one comment exists
        comment = Comment(
            user=self.user,
            entity_class='Booking',
            entity_id=1,
            content='content'
            )
        comment.save()

        comment_pk = Comment.objects.first().pk

        response = self.APP.delete(
            '/comments/%s/' % comment_pk,
            headers={'Content-Type': 'APPlication/json'}
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.filter(pk=comment_pk)
        self.assertEqual(comment.count(), 0)

    def test__filter(self):
        """
        Test get with parameters
        """

        # empty database
        Comment.objects.all().delete()

        # create few comments

        comment_1 = Comment(
            user=self.user,
            entity_id=1,
            entity_class='Booking',
            content='content'
            )
        comment_1.save()

        comment_2 = Comment(
            user=self.user,
            entity_id=1,
            entity_class='Booking',
            content='content'
            )
        comment_2.save()

        comment_3 = Comment(
            user=self.user,
            entity_id=2,
            entity_class='Booking',
            content='content'
            )
        comment_3.save()

        comment_4 = Comment(
            user=self.user,
            entity_id=1,
            entity_class='Venue',
            content='content'
            )
        comment_4.save()

        # there should be 2 comments for Booking 1 - comment_1 and comment_2
        response = self.APP.get(
            '/comments/?entity_class=Booking&entity_id=1',
            headers={'Content-Type': 'APPlication/json'}
            )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(len(data['data']), 2)
        ObjectID = comment_1.pk.__class__

        for comment in data['data']:
            self.assertTrue(ObjectID(comment['id']) in [
                comment_1.pk,
                comment_2.pk
                ])

        # delete all comments
        Comment.objects.all().delete()

    # def test__get_for_user(self):

        # user_2 = User(
            # email='asd',
            # last_name='asd',
            # first_name='asd',
            # user_id=2,
            # )

        # # empty database
        # Comment.objects.all().delete()

        # # create few comments

        # comment_1 = Comment(
            # user=self.user,
            # entity_id=1,
            # entity_class='Booking',
            # content='content'
            # )
        # comment_1.save()

        # comment_2 = Comment(
            # user=user_2,
            # entity_id=1,
            # entity_class='Booking',
            # content='content'
            # )
        # comment_2.save()

        # comment_3 = Comment(
            # user=self.user,
            # entity_id=2,
            # entity_class='Booking',
            # content='content'
            # )
        # comment_3.save()

        # comment_4 = Comment(
            # user=self.user,
            # entity_id=1,
            # entity_class='Venue',
            # content='content'
            # )
        # comment_4.save()

        # # there should be 3 comments for User 1 - c1, c3 and c4
        # response = self.APP.get(
            # '/comments/?user=' + self.user,
            # headers={'Content-Type': 'APPlication/json'}
            # )
        # self.assertEqual(response.status_code, 200)
        # data = json.loads(response.data)

        # self.assertEqual(len(data['data']), 3)
        # ObjectID = comment_1.pk.__class__

        # for comment in data['data']:
            # self.assertTrue(ObjectID(comment['id']) in [
                # comment_1.pk,
                # comment_3.pk,
                # comment_4.pk
                # ])

        # # there should be 1 comment for User 2 - c2
        # response = self.APP.get(
            # '/comments/?user_id=2',
            # headers={'Content-Type': 'APPlication/json'}
            # )
        # self.assertEqual(response.status_code, 200)
        # data = json.loads(response.data)

        # self.assertEqual(len(data['data']), 1)
        # ObjectID = comment_1.pk.__class__

        # for comment in data['data']:
            # self.assertTrue(ObjectID(comment['id']) in [comment_2.pk])

        # # there should be 0 comment for User 3
        # response = self.APP.get(
            # '/comments/?user_id=3',
            # headers={'Content-Type': 'APPlication/json'}
            # )
        # self.assertEqual(response.status_code, 200)
        # data = json.loads(response.data)

        # self.assertEqual(len(data['data']), 0)


        # # delete all comments
        # Comment.objects.all().delete()


if __name__ == '__main__': unittest.main()


