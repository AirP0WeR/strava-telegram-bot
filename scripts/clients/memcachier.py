#  -*- encoding: utf-8 -*-

import bmemcached

from common.constants_and_variables import BotVariables


class MemcachierClient:

    def __init__(self):
        self.bot_variables = BotVariables()

    def get_client(self):
        return bmemcached.Client(self.bot_variables.memcachier_servers,
                                 username=self.bot_variables.memcachier_username,
                                 password=self.bot_variables.memcachier_password)
