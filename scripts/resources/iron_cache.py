#  -*- encoding: utf-8 -*-

import logging
import traceback

import ujson

from clients.iron_cache import IronCacheClient
from common.execution_time import execution_time


class IronCacheResource:

    def __init__(self):
        self.iron_cache_client = IronCacheClient().cache()

    @execution_time
    def put_cache(self, cache, key, value):
        result = False
        try:
            logging.info("Requesting put operation on cache. Cache: %s | Key: %s | Value: %s", cache, key, value)
            self.iron_cache_client.put(cache=cache, key=key, value=value)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            result = True

        logging.info("Result: %s", result)
        return result

    @execution_time
    def get_cache(self, cache, key):
        result = False
        try:
            logging.info("Requesting get operation on cache. Cache: %s | Key: %s", cache, key)
            data = ujson.loads(self.iron_cache_client.get(cache=cache, key=key).value)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            result = data

        logging.info("Result: %s", result)
        return result
