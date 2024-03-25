# -*- coding: utf-8 -*-
"""
Created on 2019 November, 6th
@author: pjournoud
"""
from infogreffe.containers import Container

from infogreffe.db.config import Config as PostgresqlConfig
from infogreffe.db.oracle.config import Config as OracleConfig

from infogreffe.db.constants import DB_POSTGRESQL_CONFIG_FILE as POSTGRESQL_CONFIG_FILE
from infogreffe.db.constants import DB_ORACLE_CONFIG_FILE as ORACLE_CONFIG_FILE

from infogreffe.db.postgresql.connection import Connection as PostrgresqlConnection
from infogreffe.db.oracle.connection import Connection as OracleConnection

CONNECTIONS_IDENTIFIER = "CONNECTIONS"
POSTGRESQL_DATAIFG_SCORE_IDENTIFIER = "POSTGRESQL_DATAIFG_SCORE"
POSTGRESQL_DEFAULT_IDENTIFIER = "POSTGRESQL_DEFAULT"
ORACLE_DEFAULT_IDENTIFIER = "ORACLE_DEFAULT"


class ConnectionsContainer(Container):
    """
    Extraction

    """
    def __init__(self, *args):
        super(ConnectionsContainer, self).__init__(*args)


class Connections(ConnectionsContainer):
    """
    Requests factory

    """
    def __init__(self, identifier=CONNECTIONS_IDENTIFIER):
        super(Connections, self).__init__(identifier)
        self.load()

    def load(self):
        postgresql_connection_identifier = POSTGRESQL_DATAIFG_SCORE_IDENTIFIER
        config = PostgresqlConfig(
            POSTGRESQL_CONFIG_FILE,
            "DATAIFG_SCORE",
        )
        self.add(
            PostrgresqlConnection(
                postgresql_connection_identifier,
                config,
            ),
        )

        config = PostgresqlConfig(
            POSTGRESQL_CONFIG_FILE,
            "default",
        )
        postgresql_connection_identifier = POSTGRESQL_DEFAULT_IDENTIFIER
        self.add(
            PostrgresqlConnection(
                postgresql_connection_identifier,
                config,
            ),
        )

        config = PostgresqlConfig(
            ORACLE_CONFIG_FILE,
            "default",
        )
        oracle_connection_identifier = ORACLE_DEFAULT_IDENTIFIER
        self.add(
            OracleConnection(
                oracle_connection_identifier,
                config,
            ),
        )

    def get_postgresql_dataifg_score(self):
        return self.get_item(POSTGRESQL_DATAIFG_SCORE_IDENTIFIER)

    def get_identifiers(self):
        identifiers = []
        for connection in self.get_data():
            identifiers.append(connection.get_identifier())
        return identifiers

    def get_connection(self, identifier):
        return self.get_item(identifier)


if __name__ == '__main__':
    pass
