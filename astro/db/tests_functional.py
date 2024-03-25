import unittest
from pyramid import testing
import json


def _initTestingDB():

    from sqlalchemy import create_engine
    from astro.db.models import (
        DBSession,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    return DBSession


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.db = 'sqlite:////home/pjournoud/' \
                  'environments/dev/pytsprf/unittests.db'
        self.config = testing.setUp()
        self.host = 'http://localhost:6544'
        self.session = _initTestingDB()

    def tearDown(self):
        testing.tearDown()
        self.session.remove()

    def create_user(self, username, domain):

        from pytsprf.views import create_token

        request = testing.DummyRequest(params={'dbsession': self.session})
        validated_data = {'username': username,
                          'domain': domain,
                          }
        request.validated = validated_data
        request.dbsession = self.session

        request.context = json.dumps(validated_data)

        return create_token(request)

    def delete_user(self, username, domain):

        from pytsprf.views import create_token

        request = testing.DummyRequest(params={'dbsession': self.session})
        validated_data = {'username': username,
                          'domain': domain,
                          }
        request.validated = validated_data
        request.dbsession = self.session
        request.context = json.dumps(validated_data)
        response = create_token(request)
        if response.get('created'):
            from pytsprf.views import delete_user
            validated_data = {'allowed_domain': domain}
            request = testing.DummyRequest()
            request.validated = validated_data
            request.dbsession = self.session
            response = delete_user(request)
        else:
            response = None

        return response

    def test_requests(self):
        testing.DummyRequest()

    def test_create_token(self):

        username = 'create_token@unittest.com'
        domain = 'localhost:6544'

        request = testing.DummyRequest(params={'dbsession': self.session})
        validated_data = {'username': username,
                          'domain': domain,
                          }
        request.validated = validated_data
        request.dbsession = self.session

        response = self.create_user(username, domain)
        self.assertTrue(response.get('created'))

    def test_invalid_token(self):

        from pyramid.httpexceptions import HTTPUnauthorized
        from pytsprf.views import valid_token

        request = testing.DummyRequest()

        with self.assertRaises(HTTPUnauthorized):
            valid_token(request)

    def test_delete_user(self):

        username = 'delete_user@unittest.com'
        domain = 'localhost:6544'

        response = self.delete_user(username, domain)
        self.assertTrue(response.get('deleted'))
