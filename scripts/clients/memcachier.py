#  -*- encoding: utf-8 -*-

import pylibmc

from common.constants_and_variables import BotVariables


class MemcachierClient:

    def __init__(self):
        self.bot_variables = BotVariables()

    def cache(self):
        cache = pylibmc.Client(self.bot_variables.memcachier_servers, binary=True,
                               username=self.bot_variables.memcachier_username,
                               password=self.bot_variables.memcachier_password,
                               behaviors={
                                   'tcp_nodelay': True,
                                   'tcp_keepalive': True,
                                   'connect_timeout': 2000,
                                   'send_timeout': 750 * 1000,
                                   'receive_timeout': 750 * 1000,
                                   '_poll_timeout': 2000,
                                   'ketama': True,
                                   'remove_failed': 1,
                                   'retry_timeout': 2,
                                   'dead_timeout': 30
                               })
        return cache
