import pytest

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base



def test_connection():
    engine = sqlalchemy.create_engine(
        'mysql+mysqlconnector://quadrantides:Rta/Fup!wordpress0@localhost:6544/quadrantides',
        echo=True)


def _initTestingDB(path):

    from sqlalchemy import create_engine
    from astro.db.models import (
        DBSession,
        Base
        )
    engine = create_engine(path)
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    return DBSession


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.db = 'sqlite://var/lib/mysql/quadrantides.db'
        self.config = testing.setUp()
        self.host = 'http://localhost:6544'
        self.session = _initTestingDB(self.db)

    def tearDown(self):
        testing.tearDown()
        self.session.remove()

    def test_create_db_user(self):

        from astro.db.models import create_db_user

        username = 'create_db_user@unittest.com'
        allowed_domain = 'remote.server.org'
        creation, user = create_db_user(self.session,
                                        username,
                                        allowed_domain,
                                        allow_subdomains=False)
