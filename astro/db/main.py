from pyramid.config import Configurator

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (
    scoped_session, sessionmaker,
)

from astro.db.models import create_db

Session = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()
))


def get_pytsprf_config(settings):

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include("cornice")
    config.add_route('users', '/users')
    config.add_route('access', '/')
    config.add_static_view(name='assets', path='assets', cache_max_age=3600)
    config.scan()

    return config


def cli(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = create_db(settings)

    config = get_pytsprf_config(settings)

    # scoped session gives us thread safe session
    Session.configure(bind=engine)
    # make database session available in every request
    config.add_request_method(
        callable=lambda request: Session, name='dbsession', property=True)

    return config.make_wsgi_app()
