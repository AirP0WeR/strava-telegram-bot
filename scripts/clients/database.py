#  -*- encoding: utf-8 -*-

from os import sys, path

import psycopg2

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotVariables


class DatabaseClient(object):
    def __init__(self):
        self.bot_variables = BotVariables()

    def read_operation(self, query):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        database_connection.close()

        return result

    def read_all_operation(self, query):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        database_connection.close()

        return result

    def write_operation(self, query):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(query)
        cursor.close()
        database_connection.commit()
        database_connection.close()
