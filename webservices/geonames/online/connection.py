# coding=utf-8
"""
Created on 2020, Apr 3rd
@author: orion
"""
import sqlite3
from webservices.geonames.offline.constants import DB_FILE
from webservices.geonames.offline.exceptions import CursorNotAvailable


class Connection(object):
    """
    Extraction

    """

    def __init__(self):
        self.db_connection = None
        self.cursor = None

    def set_cursor(self):
        if self.db_connection:
            try:
                self.cursor = self.db_connection.cursor()

            except Exception as error:
                raise CursorNotAvailable(
                    error.__str__(),
                )

    def get_cursor(self):
        if not self.db_connection:
            self.connect()
        if not self.cursor:
            self.set_cursor()
        return self.cursor

    def close(self):
        self.get_cursor().close()
        self.db_connection.close()

        self.db_connection = None
        self.cursor = None

    def get_database_connection(self):
        return self.db_connection

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    def connect(self):
        db_connection = sqlite3.connect(DB_FILE)
        db_connection.row_factory = sqlite3.Row
        self.set_db_connection(db_connection)


if __name__ == '__main__':
    pass
