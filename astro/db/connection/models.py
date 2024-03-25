# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sqlalchemy import create_engine, text
from astro.db.config import Config


class Connection(object):

    def __init__(self, timeout=20):

        # init

        self.engine = ""
        self.timeout = 0
        self.db_connection = None
        self.config = Config(init=False)

        # settings

        self.set_engine()
        self.timeout = timeout
        # self.connect()

    def set_engine(self):
        self.config = Config()
        conf = self.config.get()
        self.engine = create_engine(
            'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                conf["user"],
                conf["password"],
                conf["host"],
                conf["port"],
                conf["dbname"],
            ),
            echo=True,
            pool_pre_ping=True,
        )

    def close(self):
        self.db_connection.close()
        self.db_connection = None

    def get_database_connection(self):
        return self.db_connection

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    def connect(self):

        try:
            self.db_connection = sqlite3.connect(self.full_filename, self.timeout)
            # this is for "by name" colums indexing
            self.db_connection.row_factory = sqlite3.Row

        except (Exception, sqlite3.DatabaseError) as error:
            raise DatabaseNotFound(
                error.__str__(),
            )

    def is_valid(self):
        return isinstance(self.db_connection, sqlite3.Connection)

    def commit(self):
        self.db_connection.commit()

    def execute(self, sql_requests):

        if isinstance(sql_requests, str):
            sql_requests = [sql_requests]
        try:
            with self.db_connection:
                for sql_request in sql_requests:
                    self.db_connection.execute(sql_request)
        except sqlite3.IntegrityError as error:
            self.close()
            raise DataIntegrityError(
                error.__str__(),
            )
        except Exception as error:
            self.close()
            raise DataUnexpectedError(
                error.__str__(),
            )


if __name__ == '__main__':

    _conn = Connection()
    with _conn.engine.connect() as conn:
        print(conn.scalar(text("select 'hi'")))
    conn.close()
    pass
