from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import (
    scoped_session, sessionmaker,
)

from pyramid.threadlocal import get_current_registry

from astro.db.conf import get_engine
from astro.db.conf import get_settings

import uuid

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def create_db(settings):

    db_session = create_db_session(settings)

    engine = get_engine(settings)
    Base.metadata.bind = engine

    # Fixme, find something more elegant
    try:
        db_session.query(User).all()

    except Exception:
        print("Creating database")
        Base.metadata.create_all(engine)

    finally:
        return engine


def create_db_session(settings=None):

    if settings is None:
        settings = get_settings()

    engine = get_engine(settings)

    session = scoped_session(sessionmaker())

    session.configure(bind=engine)
    Base.metadata.bind = engine

    return session


def _create_token():
    return uuid.uuid4().__str__()  # binascii.b2a_hex(os.urandom(20))


def get_pyramid_settings():

    settings = get_current_registry().settings
    return settings  # db_url


def get_db_users(session):

    q = session.query(User)
    if q.count() == 0:
        users = None
    else:
        users = q.all()
    return users


def get_db_user(session, allowed_domain):

    q = session.query(User).filter(User.allowed_domain == allowed_domain)
    if q.count() == 0:
        success = False
        user = None
    else:
        user = q.one()
        success = True

    return success, user


def get_db_user_token(session, allowed_domain):

    q = session.query(User).filter(User.allowed_domain == allowed_domain)
    if q.count() == 0:
        token = None
    else:
        token = q.one().htoken
    return token


def delete_db_user(session, allowed_domain):

    success, user = get_db_user(session, allowed_domain)
    if success:
        session.delete(user)
    return success


def create_db_user(session, username, allowed_domain, allow_sub_domains=False):

    is_found, user = get_db_user(session, allowed_domain)

    if is_found:
        creation = False
    else:
        new_user = User(username, allowed_domain, allow_sub_domains)
        session.add(new_user)
        creation, user = get_db_user(session, allowed_domain)

    return creation, user


def create(model, **kwargs):
    try:
        instance = model(**kwargs)
        DBSession.add(instance)
        DBSession.commit()
    except:
        DBSession.rollback()
        raise
    return instance


def delete(instance):

    DBSession.delete(instance)
    DBSession.commit()


class User(Base):
    __tablename__ = 'users'
    htoken = Column(String, primary_key=True)
    name = Column(String)
    creation_date = Column(DateTime)
    expires = Column(DateTime)
    allowed_domain = Column(String)
    allow_sub_domains = Column(Boolean)

    def __init__(self, name, allowed_domain, allow_sub_domains):
        self.htoken = _create_token()
        self.name = name
        self.allowed_domain = allowed_domain
        self.allow_sub_domains = allow_sub_domains
