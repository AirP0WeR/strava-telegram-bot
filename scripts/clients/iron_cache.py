#  -*- encoding: utf-8 -*-

from iron_cache import IronCache

from common.constants_and_variables import BotVariables


class IronCacheClient:

    def __init__(self):
        self.bot_variables = BotVariables()

    def cache(self):
        cache = IronCache(project_id=self.bot_variables.iron_cache_project_id,
                          token=self.bot_variables.iron_cache_token)
        return cache
